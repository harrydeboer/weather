import unittest
from models.DayYearArrayBuilder import DayYearArrayBuilder
from models.KNMIData import KNMIData


class TestDayYearArrayBuilder(unittest.TestCase):

    def testMakeTempArray(self):

        firstYear = 1902
        lastYear = 2019
        csvReader = KNMIData()
        tempArray = DayYearArrayBuilder.makeArray(csvReader.array, firstYear, lastYear, 'meanTemp')

        self.assertEqual(tempArray.shape, (365, lastYear - firstYear + 1))
