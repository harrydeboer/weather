import numpy as np
import datetime as dt
from models.DataColumn import DataColumn


class DateArrayBuildService:

    # An array of weather values per year and per day is made.
    @staticmethod
    def makeArray(data: np.ndarray, firstYear: int, lastYear: int, columnName: DataColumn) -> np.ndarray:

        dates = data[:, 1]

        columnNumber, factor = DataColumn[columnName].value
        column = data[:, columnNumber]
        column = column.astype(float) * factor

        # The date array is initialized with zeros.
        dayYearArray = np.zeros([365, lastYear - firstYear + 1])

        # Looping through all dates and placing the values in the dayYearArray.
        for index, date in enumerate(dates):

            # The csv file has dateformat YYYYMMDD and is split into years, months and days.
            year = int(date[:4])
            month = int(date[4:6])
            day = int(date[6:8])

            # The years outside the GUI range are neglected.
            if year < firstYear or year > lastYear:
                continue

            # The year, month and day are converted into a day number of the year.
            days_in_the_year = (dt.date(year, month, day) - dt.date(year, 1, 1)).days

            # When the year is a leap year the day number is lowered after leap day.
            # This way there are also 365 days used in the leap year.
            if year % 4 == 0 and days_in_the_year > 59:
                days_in_the_year -= 1

            dayYearArray[days_in_the_year, year - firstYear] = column[index]

        return dayYearArray
