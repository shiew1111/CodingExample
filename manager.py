from ORM.OrmMetodes import CoinsDatabase
from averagepricemonth import AveragePriceByMonth
from consecutiveincrease import ConsecutiveIncreasing
from datapresenceheck import DataPresenceCheck
from dateformatters import DatesChecker
from export import ToFile
from request import CoinPaprikaRequest


class Manager:
    def __init__(self, coin, end_date, start_date, file_name, data_format):
        self._data_format = data_format
        self._file_name = file_name
        self._start_date = start_date
        self._coin = coin
        self._end_date = end_date

    def _time_price_dict_list(self, onlyMonth=False):
        CheckDates = DatesChecker(startDate=self._start_date, endDate=self._end_date, onlyMonth=onlyMonth).check()
        self._start_date = CheckDates['startDate']
        self._end_date = CheckDates['endDate']
        time_price_from_DB = CoinsDatabase().get(self._coin, startDate=self._start_date, endDate=self._end_date)
        rangeDateList = DataPresenceCheck(startDate=CheckDates["startDate"], endDate=CheckDates["endDate"],
                                          dataFromDB=time_price_from_DB).get_range_list()
        if rangeDateList:
            for data_range in rangeDateList:
                from_api = CoinPaprikaRequest(self._coin, startDate=data_range["startDate"],
                                              endDate=data_range["endDate"]).get()

                CoinsDatabase().insert(coinName=self._coin, dataSource=from_api)
            time_price_from_DB = CoinsDatabase().get(self._coin, startDate=self._start_date, endDate=self._end_date)
        return time_price_from_DB

    def consecutive_increase(self):
        Longest_price_increasing = ConsecutiveIncreasing(self._time_price_dict_list(onlyMonth=False)).get_longest()
        return "Longest consecutive period was from {0} to {1} with increase of ${2}".format(
            Longest_price_increasing["date_from"][:-10], Longest_price_increasing["date_till"][:-10],
            round(Longest_price_increasing["price_increase"], 2))

    def average_price_by_month(self):
        average_prices_dict = AveragePriceByMonth(self._time_price_dict_list(onlyMonth=True)).get_average_price_list()
        ret_string = "Date     Average price ($)\n"
        for date, price in average_prices_dict.items():
            ret_string += "{}  {}\n".format(date, round(price, 2))

        return ret_string

    def export(self):
        ToFile(data_format=self._data_format, closePriceList=self._time_price_dict_list(onlyMonth=False),
               file_name=self._file_name).export()
        return "File ready."
