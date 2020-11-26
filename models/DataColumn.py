from enum import Enum


# This Enum has the column numbers of the data file and the factor to get to standard units.
class DataColumn(Enum):
    minTemp = (12, 10)
    meanTemp = (11, 10)
    maxTemp = (14, 10)
    windDirection = (2, 1)
    windSpeedVA = (3, 10)
    windSpeed = (4, 10)
