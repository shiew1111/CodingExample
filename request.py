from datetime import datetime, timedelta

from coinpaprika import client as Coinpaprika


from exceptions import CoinExceptionAPI


class CoinPaprikaRequest:
    def __init__(self, coin, startDate, endDate):
        self._endDate = endDate
        self._startDate = startDate
        self._coin = coin
        self._client = Coinpaprika.Client()
        self._dateRangeList = self._batches()

    def get(self):
        wholeClosePriceList = []
        for dateDict in self._dateRangeList:
            wholeClosePriceList += self._ask_API(dateDict)
        return wholeClosePriceList

    def _batches(self):
        dateRangeList = []
        if (datetime.strptime(self._endDate, '%Y-%m-%d') - (datetime.strptime(self._startDate, '%Y-%m-%d')) + timedelta(
                days=1)) > timedelta(days=334):
            dateRangeList.append({"endDate": datetime.strptime(self._startDate, '%Y-%m-%d') + timedelta(days=365),
                                  "startDate": datetime.strptime(self._startDate, '%Y-%m-%d')})
            for dateDict in dateRangeList:

                if (datetime.strptime(self._endDate, '%Y-%m-%d') - (
                        dateDict["endDate"] + timedelta(days=1))) > timedelta(days=0):
                    dateRangeList.append(
                        {"endDate": dateDict["endDate"] + timedelta(days=365),
                         "startDate": dateDict["endDate"] + timedelta(days=1)})
            dateRangeList = [{'startDate': datetime.strftime(dictOfDates['startDate'], '%Y-%m-%d'),
                              'endDate': datetime.strftime(dictOfDates['endDate'], '%Y-%m-%d')}
                             for dictOfDates in dateRangeList]
            dateRangeList[-1]['endDate'] = self._endDate
            return dateRangeList
        else:
            dateRangeList = [{"endDate": self._endDate, "startDate": self._startDate}]
            return dateRangeList

    def _bad_start_date_handle(self):
        newStartDate = self._client.coin(self._coin)["first_data_at"][:-10]
        return [self._dict_time_and_close_extract(candle_dict) for candle_dict in
                self._client.candles(self._coin, start=newStartDate, end=self._endDate)]

    def _ask_API(self, dateDict):
        try:
            closePriceList = [self._dict_time_and_close_extract(candle_dict) for candle_dict in
                              self._client.candles(self._coin, start=dateDict['startDate'], end=dateDict['endDate'])]
            if not closePriceList:
                return self._bad_start_date_handle()
            else:
                return closePriceList

        except Exception as e:
            if str(e) == "CoinpaprikaAPIException(status_code: 400): invalid parameters":

                print("You provided start-date from time before that coin existed! We used first data available.")
                return self._bad_start_date_handle()

            elif str(e) == "CoinpaprikaAPIException(status_code: 404): id not found":
                CoinExceptionAPI({"type": "Bad_coin_id", "additional_info": self._coin}).handle()

    @staticmethod
    def _dict_time_and_close_extract(candle_dict):
        return {'time_open': candle_dict['time_open'], 'close': candle_dict['close']}

