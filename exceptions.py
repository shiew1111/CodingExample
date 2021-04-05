class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class BadCoinIdError(Error):
    """Exception raised for errors caused by unknown coin id. """

    def __init__(self, expression):
        self.expression = expression
        print(
            "We couldn't find coin named ",
            self.expression,
            ". Please check coin name. ",
        )


class DatesOutOfRange(Error):
    """Exception raised for errors caused by providing dates from future. """

    def __init__(self):
        print(
            "You entered dates from the future. Please provide the appropriate dates."
        )


class DividingByZeroError(Error):
    """Exception raised for errors caused by trying to divide by 0, it may occur if somehow you will pass end_date with
    first day of month to average_price_month.py."""

    def __init__(self):
        print(
            "AveragePriceByMonth was used with bad date. end-date shouldn't be like 2021-03-01."
        )


class NotMatchingFileFormats(Error):
    """Exception raised for errors caused by not matching provided format with format in provided file name. """

    def __init__(self):
        print("You provided different file formats in file_name and format.")


class InvalidDateFormat(Error):
    """Exception raised for errors caused by providing invalid date formats. """

    def __init__(self):
        print("Expects a valid date format. Examples: 2021-03 or 2021-03-01 ")
