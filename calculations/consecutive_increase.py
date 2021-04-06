from datetime import datetime

from data_classes import PriceIncreaseRange


class ConsecutiveIncreasing:
    """It finds longest price increase. It takes list of dictionary's [ {'time_open': str', 'close': float}].
    Example output: {'date_from': str, 'date_till': str, 'price_increase': float}
    """

    def __init__(self, closePriceList: list):

        self._close_price_list = closePriceList
        self._longestConsecutiveIncreasing = PriceIncreaseRange(
            date_from=self._close_price_list[0].time_open,
            date_till=self._close_price_list[0].time_open,
            price_increase=0,
        )
        self._priceIncreasingCurrent = PriceIncreaseRange(
            date_from=self._close_price_list[0].time_open,
            date_till=self._close_price_list[0].time_open,
            price_increase=0,
        )
        self._calculate_consecutive_increasing()

    def _check_first_two_price(self):
        if self._close_price_list[1].close < self._close_price_list[0].close:
            self._priceIncreasingCurrent.update_date_from(
                self._close_price_list[1].time_open
            )

    def _current_price_increasing_length(self):
        return datetime.strptime(
            self._priceIncreasingCurrent.date_till[:-10], "%Y-%m-%d"
        ) - datetime.strptime(self._priceIncreasingCurrent.date_from[:-10], "%Y-%m-%d")

    def _longest_price_increasing(self):
        return datetime.strptime(
            self._longestConsecutiveIncreasing.date_till[:-10], "%Y-%m-%d"
        ) - datetime.strptime(
            self._longestConsecutiveIncreasing.date_from[:-10], "%Y-%m-%d"
        )

    def _reset_current_price_increasing(self, index):
        self._priceIncreasingCurrent.update_all(
            new_date_till=self._close_price_list[index].time_open,
            new_date_from=self._close_price_list[index].time_open,
            new_price_increase=0,
        )

    def _calculate_consecutive_increasing(self):

        for priceDict in range(1, len(self._close_price_list)):
            if (
                self._close_price_list[priceDict].close
                > self._close_price_list[priceDict - 1].close
            ):

                self._priceIncreasingCurrent.update_date_till(
                    self._close_price_list[priceDict].time_open
                )
                self._priceIncreasingCurrent.update_price_increase(
                    self._priceIncreasingCurrent.price_increase
                    + (
                        self._close_price_list[priceDict].close
                        - self._close_price_list[priceDict - 1].close
                    )
                )

            elif (
                self._current_price_increasing_length()
                > self._longest_price_increasing()
            ):
                self._longestConsecutiveIncreasing.update_all(
                    new_date_from=self._priceIncreasingCurrent.date_from,
                    new_date_till=self._priceIncreasingCurrent.date_till,
                    new_price_increase=self._priceIncreasingCurrent.price_increase,
                )
                self._reset_current_price_increasing(priceDict)
            else:
                self._reset_current_price_increasing(priceDict)

    def get_longest(self):
        return self._longestConsecutiveIncreasing
