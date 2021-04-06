from exceptions import DividingByZeroError


class AveragePriceByMonth:
    """It calculate average price by month. It takes list of dictionary's [ {'time_open': str', 'close': float}].
    Example output:  {'2021-01': float, '2021-02': float, '2021-03': float}"""

    def __init__(self, closePriceList: list):
        self._close_price_list = closePriceList
        self._time_open_trim()
        self._average_price_dict = self._calculate_average_by_month()

    def get_average_price_list(self):
        return self._average_price_dict

    def _time_open_trim(self):
        for priceDict in self._close_price_list:
            priceDict.trim_time_open()

    def _calculate_average_by_month(self):
        average_price_dict = {self._close_price_list[0].time_open: 0}
        day_of_month_index = 1
        previous_time_open = self._close_price_list[0].time_open
        for priceDict in range(len(self._close_price_list)):
            if self._close_price_list[priceDict].time_open == previous_time_open:
                try:
                    average_price_dict[
                        self._close_price_list[priceDict].time_open
                    ] += float(self._close_price_list[priceDict].close)
                except KeyError:
                    average_price_dict[self._close_price_list[priceDict].time_open] = 0
                day_of_month_index += 1
            else:
                average_price_dict[self._close_price_list[priceDict - 1].time_open] /= (
                    day_of_month_index - 1
                )
                day_of_month_index = 1
            if priceDict == len(self._close_price_list) - 1:
                try:
                    average_price_dict[
                        self._close_price_list[priceDict - 1].time_open
                    ] /= (day_of_month_index - 1)
                except ZeroDivisionError:
                    raise DividingByZeroError()
            previous_time_open = self._close_price_list[priceDict].time_open
        return average_price_dict
