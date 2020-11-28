import unittest
from services.DateArrayBuildService import DateArrayBuildService
from models.KNMIData import KNMIData


class TestDayYearArrayBuilder(unittest.TestCase):

    def testMakeTempArray(self):

        firstYear = 1904
        lastYear = 2019
        csvReader = KNMIData()
        tempArray = DateArrayBuildService.makeArray(csvReader.array, firstYear, lastYear, 'meanTemp')

        self.assertEqual(tempArray.shape, (365, lastYear - firstYear + 1))
