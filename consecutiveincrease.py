from datetime import datetime


class ConsecutiveIncreasing:
    def __init__(self, closePriceList):

        self._close_price_list = closePriceList
        self._longestConsecutiveIncreasing = {"date_from": self._close_price_list[0]["time_open"],
                                              "date_till": self._close_price_list[0]["time_open"],
                                              "price_increase": 0}

        self._priceIncreasingCurrent = {"date_from": self._close_price_list[0]["time_open"],
                                        "date_till": self._close_price_list[0]["time_open"],
                                        "price_increase": 0}
        self._calculate_consecutive_increasing()

    def _check_first_two_price(self):
        if self._close_price_list[1]["close"] < self._close_price_list[0]["close"]:
            self._priceIncreasingCurrent.update({"date_from": self._close_price_list[1]["time_open"]})

    def _current_price_increasing_length(self):
        return datetime.strptime(self._priceIncreasingCurrent["date_till"][:-10], '%Y-%m-%d') - datetime.strptime(
            self._priceIncreasingCurrent["date_from"][:-10], '%Y-%m-%d')

    def _longest_price_increasing(self):
        return datetime.strptime(self._longestConsecutiveIncreasing["date_till"][:-10], '%Y-%m-%d') - datetime.strptime(
            self._longestConsecutiveIncreasing["date_from"][:-10], '%Y-%m-%d')

    def _reset_current_price_increasing(self, index):
        self._priceIncreasingCurrent.update(
            {"date_till": self._close_price_list[index]["time_open"],
             "date_from": self._close_price_list[index]["time_open"],
             "price_increase": 0})

    def _calculate_consecutive_increasing(self):

        for priceDict in range(1, len(self._close_price_list)):

            if self._close_price_list[priceDict]["close"] > self._close_price_list[priceDict - 1]["close"]:
                self._priceIncreasingCurrent.update(
                    {"date_till": self._close_price_list[priceDict]["time_open"],
                     "price_increase": self._priceIncreasingCurrent['price_increase'] + (
                             self._close_price_list[priceDict]["close"] -
                             self._close_price_list[priceDict - 1]["close"])})

            elif self._current_price_increasing_length() > self._longest_price_increasing():
                self._longestConsecutiveIncreasing.update(
                    {"date_from": self._priceIncreasingCurrent["date_from"],
                     "date_till": self._priceIncreasingCurrent["date_till"],
                     "price_increase": self._priceIncreasingCurrent["price_increase"]})
                self._reset_current_price_increasing(priceDict)
            else:
                self._reset_current_price_increasing(priceDict)

    def get_longest(self):
        return self._longestConsecutiveIncreasing

#
# CheckDates = DatesChecker(startDate="2011-03-01", endDate="2021-03-30", onlyMonth=False).check()
# print(CheckDates)
#
# print(ConsecutiveIncreasing(CoinPaprikaRequest("bnb-binance-coin", startDate=CheckDates["startDate"],
#                                               endDate=CheckDates["endDate"]).get()).get_longest())
