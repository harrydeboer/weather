import unittest
from services.DateArrayBuildService import DateArrayBuildService
from models.KNMIData import KNMIData
from models.DataColumn import DataColumn


class TestDayYearArrayBuilder(unittest.TestCase):

    def testMakeTempArray(self):

        firstYear = 1904
        lastYear = 2019
        knmiData = KNMIData()
        tempArray = DateArrayBuildService.makeArray(knmiData.array, firstYear, lastYear, DataColumn.meanTemp)

        self.assertEqual(tempArray.shape, (365, lastYear - firstYear + 1))
