from enum import Enum


# This Enum has the column numbers of the KNMI data file and the factor to get to standard units (SI units).
class DataColumn(Enum):

    # (column_number, factor)
    min_temp = (12, 0.1)
    mean_temp = (11, 0.1)
    max_temp = (14, 0.1)
    wind_direction = (2, 1)
    wind_speed_va = (3, 0.1)
    wind_speed = (4, 0.1)
    perc_sunshine = (19, 1)
    perc_rain = (21, 0.416666666666)
    amount_rain = (22, 0.1)
