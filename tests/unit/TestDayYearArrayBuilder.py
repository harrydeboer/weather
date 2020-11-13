import unittest
from models.DayYearArrayBuilder import DayYearArrayBuilder
from models.CsvReader import CsvReader


class TestDayYearArrayBuilder(unittest.TestCase):

    def testMakeTempArray(self):

        firstYear = 1902
        lastYear = 2019
        csvReader = CsvReader()
        tempArray = DayYearArrayBuilder.makeArray(csvReader.csvArray, firstYear, lastYear, 'meanTemp')

        self.assertEqual(tempArray.shape, (365, lastYear - firstYear + 1))
