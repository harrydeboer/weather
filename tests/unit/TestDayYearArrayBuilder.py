import unittest
from services.DayYearArrayBuildService import DayYearArrayBuildService
from models.KNMIData import KNMIData
from models.DataColumn import DataColumn


class TestDayYearArrayBuilder(unittest.TestCase):

    def testMakeTempArray(self):

        first_year = 1906
        last_year = 2019
        knmi_data = KNMIData()
        temp_array = DayYearArrayBuildService.make_array(knmi_data.array, first_year, last_year, DataColumn.mean_temp)

        self.assertEqual(temp_array.shape, (365, last_year - first_year + 1))
