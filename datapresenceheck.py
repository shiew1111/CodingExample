from datetime import timedelta, datetime


class DataPresenceCheck:
    def __init__(self, startDate, endDate, dataFromDB):
        self._dataFromDB = dataFromDB
        self._endDate = endDate
        self._startDate = startDate

    def _date_list(self):
        startDate = datetime.strptime(self._startDate, '%Y-%m-%d')
        delta = datetime.strptime(self._endDate, '%Y-%m-%d') - startDate
        return [datetime.strftime(startDate + timedelta(days=i), '%Y-%m-%dT%H:%M:%SZ') for i in range(delta.days + 1)]

    def _trim_date_list(self):
        return [date for date in self._date_list() if date not in [dbDate['time_open'] for dbDate in self._dataFromDB]]

    def get_range_list(self):
        dateList = self._trim_date_list()
        rangeDateList = []
        if dateList:

            firstException = True
            y = 0
            if len(dateList) != 1:
                for i in range(1, len(dateList)):
                    currentDate = datetime.strptime(dateList[i], '%Y-%m-%dT%H:%M:%SZ')
                    if (currentDate != datetime.strptime(dateList[i - 1], '%Y-%m-%dT%H:%M:%SZ') + timedelta(
                            days=1)):
                        if firstException:
                            rangeDateList.append({'startDate': dateList[0], 'endDate': dateList[i - 1]})
                            firstException = False
                            y = i

                        else:
                            rangeDateList.append({'startDate': dateList[y], 'endDate': dateList[i - 1]})
                            y = i
                    elif i == len(dateList) - 1:
                        rangeDateList.append({'startDate': dateList[y], 'endDate': dateList[i]})
            else:
                rangeDateList.append({'startDate': dateList[0], 'endDate': dateList[0]})

            rangeDateList = [{'startDate': rangeDict["startDate"][:10], 'endDate': rangeDict["endDate"][:10]} for rangeDict in rangeDateList ]
        return rangeDateList


