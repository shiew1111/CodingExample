from datetime import datetime, timedelta

from exceptions import DatesOutOfRange


class DatesChecker:
    """Extensive validation of user-entered dates. Depending on your needs, it will return the dates containing days
    or just year and month. It can take, datetime object's or string's like "2021-01-01" or "2021-03". Also it checks
    if start date isn't newer than end date, and if end date is not out of range. If user will enter date without
    day's. And we will pass onlyMonth=False, it will return start date with first day of provided month and end date
    with last day of provided month."""

    def __init__(self, startDate, endDate, onlyMonth=False):
        self._onlyMonth = onlyMonth
        self._startDate = startDate
        self._endDate = endDate
        self._check_is_date_datetime()
        self._format_select()
        self._dates_placement_check()
        self._from_only_month_valid_date()

    def _check_is_date_datetime(self):
        if isinstance(self._startDate, datetime):
            self._startDate = datetime.strftime(self._startDate, "%Y-%m-%dT%H:%M:%SZ")[
                :-10
            ]
        if isinstance(self._endDate, datetime):
            self._endDate = datetime.strftime(self._endDate, "%Y-%m-%dT%H:%M:%SZ")[:-10]

    def _end_date_last_day_month(self):
        datetime.strptime(self._endDate, "%Y-%m")
        month = int(self._endDate[-2:].lstrip("0"))
        if month < 9:
            self._endDate = str(int(self._endDate[:-3])) + "-0" + str(month + 1) + "-01"
        elif 12 > month >= 9:
            self._endDate = str(int(self._endDate[:-3])) + "-" + str(month + 1) + "-01"
        elif month == 12:
            self._endDate = str(int(self._endDate[:-3]) + 1) + "-01-01"
        self._endDate = datetime.strptime(self._endDate, "%Y-%m-%d") - timedelta(days=1)
        self._endDate = datetime.strftime(self._endDate, "%Y-%m-%d")

    def _from_only_month_valid_date(self):
        if self._onlyMonth:
            self._end_date_last_day_month()
            self._startDate = datetime.strftime(
                datetime.strptime(self._startDate + "-01", "%Y-%m-%d"), "%Y-%m-%d"
            )
            self._date_max_check(dateFormat="%Y-%m-%d")

    def check(self):
        return {"startDate": self._startDate, "endDate": self._endDate}

    # Check if end date is not higher than present, if it is, than present become end-date
    def _date_max_check(self, dateFormat):
        present = datetime.strftime(datetime.now(), dateFormat)
        if (self._endDate > present) & (self._startDate > present):
            raise DatesOutOfRange()
        elif self._endDate > present:
            self._endDate = present
        elif self._startDate > present:
            self._startDate = present

    def _only_month_date(self):
        try:
            datetime.strptime(self._startDate, "%Y-%m")
        except ValueError:
            datetime.strptime(self._startDate, "%Y-%m-%d")
            self._startDate = self._startDate[:-3]

        try:
            datetime.strptime(self._endDate, "%Y-%m")
        except ValueError:
            datetime.strptime(self._endDate, "%Y-%m-%d")
            self._endDate = self._endDate[:-3]

    def _full_date(self):
        try:
            datetime.strptime(self._startDate, "%Y-%m-%d")
        except ValueError:
            self._startDate = self._startDate + "-01"
            datetime.strptime(self._startDate, "%Y-%m-%d")
            print(
                "You provided bad date format for that function. We added days (start-date=",
                self._startDate,
                ") to your dates!",
            )

        try:
            datetime.strptime(self._endDate, "%Y-%m-%d")
        except ValueError:
            self._end_date_last_day_month()
            datetime.strptime(self._endDate, "%Y-%m-%d")
            print(
                "You provided bad date format for that function. We added days ( end-date=",
                self._endDate,
                ") to your dates!",
            )

    def _dates_placement_check(self):

        if self._startDate > self._endDate:
            self._startDate, self._endDate = self._endDate, self._startDate

            print(
                "The start date is newer than the end date. The dates have been swapped."
            )

    def _format_select(self):
        if self._onlyMonth:
            self._only_month_date()

        else:
            self._full_date()
            self._date_max_check(dateFormat="%Y-%m-%d")
