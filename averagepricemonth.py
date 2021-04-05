from exceptions import CoinExceptionAPI


class AveragePriceByMonth:
    def __init__(self, closePriceList):
        self._close_price_list = closePriceList
        self._time_open_trim()
        self._average_price_dict = self._calculate_average_by_month()

    def get_average_price_list(self):
        return self._average_price_dict

    def _time_open_trim(self):
        for priceDict in range(len(self._close_price_list)):
            self._close_price_list[priceDict]["time_open"] = self._close_price_list[priceDict]["time_open"][:-13]

    def _calculate_average_by_month(self):
        average_price_dict = {self._close_price_list[0]["time_open"]: 0}
        dayOfMonthIndex = 1
        previousTimeOpen = self._close_price_list[0]["time_open"]
        for priceDict in range(len(self._close_price_list)):
            if self._close_price_list[priceDict]["time_open"] == previousTimeOpen:
                try:
                    average_price_dict[self._close_price_list[priceDict]["time_open"]] += float(
                        self._close_price_list[priceDict]["close"])
                except KeyError:
                    average_price_dict[self._close_price_list[priceDict]["time_open"]] = 0
                dayOfMonthIndex += 1
            else:
                average_price_dict[self._close_price_list[priceDict - 1]["time_open"]] /= dayOfMonthIndex - 1
                dayOfMonthIndex = 1
            if priceDict == len(self._close_price_list) - 1:
                try:
                    average_price_dict[self._close_price_list[priceDict - 1]["time_open"]] /= dayOfMonthIndex - 1
                except ZeroDivisionError:
                    CoinExceptionAPI({"type": "ZeroDivisionError_AveragePriceByMonth"}).handle()
            previousTimeOpen = self._close_price_list[priceDict]["time_open"]

        return average_price_dict

