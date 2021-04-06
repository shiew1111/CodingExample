from datetime import datetime, timedelta

from coinpaprika import client as Coinpaprika

from data_classes import DateRange, DayPrice
from exceptions import BadCoinIdError


class CoinPaprikaRequest:
    """It's responsible for requesting data from API. Because API max response is 366 rows(days), it provided max
    batch size and request data in few requests if needed."""

    def __init__(self, coin, startDate, endDate):
        self._endDate = endDate
        self._startDate = startDate
        self._coin = coin
        self._client = Coinpaprika.Client()
        self._dateRangeList = self._batches()

    def get(self):
        whole_close_price_list = []
        for date_dict in self._dateRangeList:
            whole_close_price_list += self._ask_API(date_dict)
        return whole_close_price_list

    def _batches(self):
        date_range_list = []
        if (
            datetime.strptime(self._endDate, "%Y-%m-%d")
            - (datetime.strptime(self._startDate, "%Y-%m-%d"))
            + timedelta(days=1)
        ) <= timedelta(days=334):
            date_range_list = [
                DateRange(startDate=self._startDate, endDate=self._endDate)
            ]
            return date_range_list
        date_range_list.append(
            DateRange(
                startDate=datetime.strptime(self._startDate, "%Y-%m-%d")
                + timedelta(days=365),
                endDate=datetime.strptime(self._startDate, "%Y-%m-%d"),
            )
        )
        for date_dict in date_range_list:

            if (
                datetime.strptime(self._endDate, "%Y-%m-%d")
                - (date_dict.endDate + timedelta(days=1))
            ) > timedelta(days=0):
                date_range_list.append(
                    DateRange(
                        startDate=date_dict.endDate + timedelta(days=365),
                        endDate=date_dict.endDate + timedelta(days=1),
                    )
                )
        date_range_list = [
            DateRange(
                startDate=datetime.strftime(dictOfDates.startDate, "%Y-%m-%d"),
                endDate=datetime.strftime(dictOfDates.endDate, "%Y-%m-%d"),
            )
            for dictOfDates in date_range_list
        ]
        date_range_list[-1].endDate = self._endDate
        return date_range_list

    def _bad_start_date_handle(self):
        new_start_date = self._client.coin(self._coin)["first_data_at"][:-10]
        return [
            self._dict_time_and_close_extract(candle_dict)
            for candle_dict in self._client.candles(
                self._coin, start=new_start_date, end=self._endDate
            )
        ]

    def _ask_API(self, dateDict):
        try:
            close_price_list = [
                self._dict_time_and_close_extract(candle_dict)
                for candle_dict in self._client.candles(
                    self._coin, start=str(dateDict.startDate), end=str(dateDict.endDate)
                )
            ]
            if not close_price_list or None:
                return self._bad_start_date_handle()
            else:
                return close_price_list

        except Exception as e:
            if (
                str(e)
                == "CoinpaprikaAPIException(status_code: 400): invalid parameters"
            ):

                print(
                    "You provided start-date from time before that coin existed! We used first data available."
                )
                return self._bad_start_date_handle()

            elif str(e) == "CoinpaprikaAPIException(status_code: 404): id not found":
                raise BadCoinIdError(self._coin)

    @staticmethod
    def _dict_time_and_close_extract(candle_dict):
        return DayPrice(time_open=candle_dict["time_open"], close=candle_dict["close"])
