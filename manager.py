from ORM.orm_get_insert import CoinsDatabase
from calculations.average_price_month import AveragePriceByMonth
from calculations.consecutive_increase import ConsecutiveIncreasing
from data_presence_check import DataPresenceCheck
from date_formatters import DatesChecker
from export import ToFile
from request import CoinPaprikaRequest


class Manager:
    """ It takes all valid arguments, provided by user, and pass further. """

    def __init__(self, coin, end_date, start_date, file_name, data_format):
        self._data_format = data_format
        self._file_name = file_name
        self._start_date = start_date
        self._coin = coin
        self._end_date = end_date
        self._coin_database = CoinsDatabase()

    def _time_price_dict_list(self, onlyMonth: bool = False):
        # named tuple zrobić
        check_dates_range = DatesChecker(
            startDate=self._start_date, endDate=self._end_date, onlyMonth=onlyMonth
        ).check()
        self._start_date = check_dates_range.startDate
        self._end_date = check_dates_range.endDate
        time_price_from_DB = self._coin_database.get(
            self._coin, startDate=self._start_date, endDate=self._end_date
        )
        range_date_list = DataPresenceCheck(
            startDate=check_dates_range.startDate,
            endDate=check_dates_range.endDate,
            dataFromDB=time_price_from_DB,
        ).get_range_list()
        if range_date_list:
            for data_range in range_date_list:
                from_api = CoinPaprikaRequest(
                    self._coin,
                    startDate=data_range.startDate,
                    endDate=data_range.endDate,
                ).get()

                self._coin_database.insert(coinName=self._coin, dataSource=from_api)
            time_price_from_DB = self._coin_database.get(
                self._coin, startDate=self._start_date, endDate=self._end_date
            )
        return time_price_from_DB

    def consecutive_increase(self):
        Longest_price_increasing = ConsecutiveIncreasing(
            self._time_price_dict_list(onlyMonth=False)
        ).get_longest()
        return "Longest consecutive period was from {0} to {1} with increase of ${2}".format(
            Longest_price_increasing.date_from[:-10],
            Longest_price_increasing.date_till[:-10],
            round(Longest_price_increasing.price_increase, 2),
        )

    def average_price_by_month(self):
        average_prices_dict = AveragePriceByMonth(
            self._time_price_dict_list(onlyMonth=True)
        ).get_average_price_list()
        ret_string = "Date     Average price ($)\n"
        for date, price in average_prices_dict.items():
            ret_string += "{}  {}\n".format(date, round(price, 2))

        return ret_string

    def export(self):
        ToFile(
            data_format=self._data_format,
            close_price_list=self._time_price_dict_list(onlyMonth=False),
            file_name=self._file_name,
        ).export()
        return "File ready."
