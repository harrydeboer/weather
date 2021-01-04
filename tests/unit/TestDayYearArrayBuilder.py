import unittest
from services.DayYearArrayBuildService import DayYearArrayBuildService
from models.KNMIData import KNMIData
from models.DataColumn import DataColumn


class TestDayYearArrayBuilder(unittest.TestCase):

    def testMakeTempArray(self):

        firstYear = 1906
        lastYear = 2019
        knmiData = KNMIData()
        tempArray = DayYearArrayBuildService.makeArray(knmiData.array, firstYear, lastYear, DataColumn.meanTemp)

        self.assertEqual(tempArray.shape, (365, lastYear - firstYear + 1))
