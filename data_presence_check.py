from datetime import timedelta, datetime
from data_classes import DateRange


class DataPresenceCheck:
    """It's responsible for checking, if data from database covers date range provided by user. If not it return list
    of date range's needed to be covered."""

    def __init__(self, startDate, endDate, dataFromDB):
        self._dataFromDB = dataFromDB
        self._endDate = endDate
        self._startDate = startDate

    def _date_list(self):
        startDate = datetime.strptime(self._startDate, "%Y-%m-%d")
        delta = datetime.strptime(self._endDate, "%Y-%m-%d") - startDate
        return [
            datetime.strftime(startDate + timedelta(days=i), "%Y-%m-%dT%H:%M:%SZ")
            for i in range(delta.days + 1)
        ]

    def _trim_date_list(self):
        return [
            date
            for date in self._date_list()
            if date not in [dbDate.time_open for dbDate in self._dataFromDB]
        ]

    def get_range_list(self):
        date_list = self._trim_date_list()
        range_date_list = []
        if date_list:

            firstException = True
            y = 0
            if len(date_list) != 1:
                for i in range(1, len(date_list)):
                    currentDate = datetime.strptime(date_list[i], "%Y-%m-%dT%H:%M:%SZ")
                    if currentDate != datetime.strptime(
                        date_list[i - 1], "%Y-%m-%dT%H:%M:%SZ"
                    ) + timedelta(days=1):
                        if firstException:

                            range_date_list.append(
                                DateRange(
                                    startDate=date_list[0], endDate=date_list[i - 1]
                                )
                            )
                            firstException = False
                            y = i

                        else:
                            range_date_list.append(
                                DateRange(
                                    startDate=date_list[y], endDate=date_list[i - 1]
                                )
                            )
                            y = i
                    elif i == len(date_list) - 1:
                        range_date_list.append(
                            DateRange(startDate=date_list[y], endDate=date_list[i])
                        )
            else:
                range_date_list.append(
                    DateRange(startDate=date_list[0], endDate=date_list[0])
                )

            range_date_list = [
                DateRange(
                    startDate=range_dict.startDate[:10], endDate=range_dict.endDate[:10]
                )
                for range_dict in range_date_list
            ]
        return range_date_list
