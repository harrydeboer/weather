from enum import Enum


# This Enum has the column numbers of the KNMI data file and the factor to get to standard units (SI units).
class DataColumn(Enum):

    # (columnNumber, factor)
    minTemp = (12, 0.1)
    meanTemp = (11, 0.1)
    maxTemp = (14, 0.1)
    windDirection = (2, 1)
    windSpeedVA = (3, 0.1)
    windSpeed = (4, 0.1)
