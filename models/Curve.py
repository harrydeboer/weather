import numpy as np
import datetime as dt


class Curve:

    def __init__(self, y: np.ndarray, isDayCurve: bool, firstYear: int, lastYear: int):

        if isDayCurve:
            x = np.arange(1, 366)
        else:
            x = np.arange(firstYear, lastYear + 1)

        self.x = x
        boxPoints = 30

        # If isDayCurve the smooth curve is made over three times the original array.
        # That way the endpoints of the inbetween array match. For the year curve the reverse curve is added.
        if isDayCurve:
            ySmooth = self.__makeSmoothCurve(np.append(y, [y, y]), boxPoints)
        else:
            ySmooth = self.__makeSmoothCurveLinearExtrapolate(y, boxPoints)

        self.y = y

        if isDayCurve:
            length = int(ySmooth.size / 3)
            self.ySmooth = ySmooth[length: 2 * length]
        else:
            self.ySmooth = ySmooth

    @staticmethod
    def __makeSmoothCurve(y, boxPoints) -> np.ndarray:

        box = np.ones(boxPoints) / boxPoints
        result = np.convolve(y, box, mode='same')

        return result

    # A moving average is used to smooth the curve. At the edges the data is extrapolated linearly with a regression.
    # That way the smoothing behaves well at the edges.
    @classmethod
    def __makeSmoothCurveLinearExtrapolate(cls, y, boxPoints) -> np.ndarray:

        yregress = y[:boxPoints]
        xregress = np.arange(0, boxPoints)

        alpha, beta = cls.__calculateAlphaBeta(yregress, xregress)

        yprepend = np.arange(boxPoints * (-1), 0) * beta + alpha

        yregress = y[-boxPoints:]
        xregress = np.arange(y.size - boxPoints, y.size)

        alpha, beta = cls.__calculateAlphaBeta(yregress, xregress)

        yappend = np.arange(y.size, y.size + boxPoints) * beta + alpha

        box = np.ones(boxPoints) / boxPoints
        result = np.convolve(np.append(np.append(yprepend, y), yappend), box, mode='same')

        return result[boxPoints:-boxPoints]

    @staticmethod
    def __calculateAlphaBeta(yregress: np.ndarray, xregress: np.ndarray):

        ymean = yregress.mean()
        xmean = xregress.mean()

        beta = np.sum((xregress - xmean) * (yregress - ymean)) / np.sum((xregress - xmean) * (xregress - xmean))
        alpha = ymean - beta * xmean

        return alpha, beta

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

        # The KNMI angle starts at 0 (north) and goes clockwise to 360 degrees.
        # The x and y coordinates are calculated because a mean can only be taken from x and y coordinates.
        x = speed2D * np.sin(angle2D / 360 * 2 * np.pi)
        y = speed2D * np.cos(angle2D / 360 * 2 * np.pi)
        xmean = x.mean(1)
        ymean = y.mean(1)

        angle = np.zeros(365)

        for index, value in enumerate(xmean):
            angle[index] = np.arctan2(ymean[index], xmean[index]) / np.pi * 180

            # The arctan2 function start at -Pi (west) and goes counterclockwise to Pi.
            # The angle starts at 0 (east) and goes to 360.
            # There is a gap of 2 Pi in the west point and this gap is closed
            # by adding 360 degrees when y < 0 (y changes sign in the west point).
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
