from scipy.signal import savgol_filter
from numpy.linalg import LinAlgError
import numpy as np
import math
import datetime as dt


class Curve:

    def __init__(self, y: np.ndarray, isDayCurve: bool, firstYear: int, lastYear: int):

        if isDayCurve == 1:
            x = np.arange(1, 366)
        else:
            x = np.arange(firstYear, lastYear + 1)

        # The Savitzky-Golay filter needs an odd valued window.
        # The window is one third the size of the curve and then made an odd integer.
        window = int(y.size / 3)
        if window % 2 == 0:
            window += 1
        window = max(5, window)

        # If isTriple the smooth curve is made over three times the original array.
        # That way the endpoints of the in between array match.
        if isDayCurve == 1:
            ySmooth = self.__makeSmoothCurve(np.append(y, [y, y]), window)
        else:
            ySmooth = self.__makeSmoothCurve(y, window)

        self.x = x
        self.y = y
        if isDayCurve == 1:
            self.ySmooth = ySmooth[365:730]
        else:
            self.ySmooth = ySmooth

    # The Savitzky-Golay savgol_filter function does not always work right away.
    # The same input is given untill there is no exception.
    def __makeSmoothCurve(self, y, window) -> np.ndarray:

        try:
            result = savgol_filter(y, window, 3)
        except LinAlgError:
            result = self.__makeSmoothCurve(y, window)

        return result

    # The first day of summer is the point where the temperature is equal to the temperature 92 days later.
    # On average a season has 92 days. The smooth curves are substracted with 92 days interval.
    # Then the absolute value is taken.
    # Then the first day of summer is the point where these absolute values are minimal.
    # Then the first day is translated into a date object.
    def getFirstDateSummer(self) -> dt:

        subtract = np.subtract(self.ySmooth[92:], self.ySmooth[:365 - 92])
        firstDayOfSummer = int(np.where(np.absolute(subtract) == np.min(np.absolute(subtract)))[0][0])

        return dt.datetime(2019, 1, 1) + dt.timedelta(firstDayOfSummer)

    @staticmethod
    def meanOfAngle(speed2D: np.ndarray, angle2D: np.ndarray) -> np.ndarray:

        x = speed2D * np.sin(angle2D / 360 * 2 * math.pi)
        y = speed2D * np.cos(angle2D / 360 * 2 * math.pi)
        xmean = x.mean(1)
        ymean = y.mean(1)

        angle = np.zeros(365)

        for index, value in enumerate(xmean):
            radius = math.sqrt(ymean[index] * ymean[index] + xmean[index] * xmean[index])

            angle[index] = math.atan2(ymean[index] / radius, xmean[index] / radius) / math.pi * 180

            if ymean[index] < 0:
                angle[index] += 360

        return angle

    # The curve can have a mean per month if it is a day curve.
    @staticmethod
    def getMonthMean(y: np.ndarray, month: int, year: int) -> float:

        if y.size != 365:
            raise Exception('This stat can only be calculated for day curves.')

        dayNumberBegin = dt.datetime(year, month, 1).timetuple().tm_yday
        if month == 12:
            dayNumberEnd = dt.datetime(year, month, 31).timetuple().tm_yday
        else:
            dayNumberEnd = dt.datetime(year, month + 1, 1).timetuple().tm_yday - 1

        return y[dayNumberBegin - 1:dayNumberEnd].mean(axis=0)
