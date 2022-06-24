import unittest
from weather.services import DayYearArrayBuildService
from weather.models import KNMIData
from weather.models import DataColumn


class TestDayYearArrayBuilder(unittest.TestCase):

    def testMakeTempArray(self) -> None:

        first_year = 1906
        last_year = 2019
        knmi_data = KNMIData()
        temp_array = DayYearArrayBuildService.make_array(knmi_data.array, first_year, last_year, DataColumn.mean_temp)

        self.assertEqual(temp_array.shape, (365, last_year - first_year + 1))
