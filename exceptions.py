class CoinExceptionAPI(Exception):
    def __init__(self, exceptionDict):
        self._exceptionType = exceptionDict

    def handle(self):
        if self._exceptionType["type"] == "Bad_coin_id":
            print("We couldn't find coin named ", self._exceptionType["additional_info"], ". Please check coin name. ")
            raise SystemExit(1)
        elif self._exceptionType["type"] == "Dates_out_of_range":
            print("You entered dates from the future. Please provide the appropriate dates.")
            raise SystemExit(1)
        elif self._exceptionType["type"] == "ZeroDivisionError_AveragePriceByMonth":
            print("AveragePriceByMonth was used with bad date. end-date shouldn't be like 2021-03-01.")
            raise SystemExit(1)
        elif self._exceptionType["type"] == "File_formats_not_match":
            print("You provided different file formats in file_name and format.")
            raise SystemExit(1)
        elif self._exceptionType["type"] == "Invalid_date_format":
            print("Expects a valid date format. Examples: 2021-03 or 2021-03-01 ")
            raise SystemExit(1)
