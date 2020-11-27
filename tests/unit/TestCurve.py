import unittest
import numpy as np
import datetime as datetime
from services.DateArrayBuildService import DateArrayBuildService
from models.KNMIData import KNMIData
from models.Curve import Curve


class TestCurve(unittest.TestCase):

    def setUp(self):

        self.firstYear = 1902
        self.lastYear = 2019
        csvReader = KNMIData()
        tempArray = DateArrayBuildService.makeArray(csvReader.array, self.firstYear, self.lastYear, 'meanTemp')
        self.curve = Curve(tempArray, True, self.firstYear, self.lastYear)

    def testAverTempSmooth(self):

        self.assertEqual(self.curve.ySmooth.size, 365)

    def testFirstDateSummer(self):

        date = self.curve.getFirstDateSummer()

        self.assertIsInstance(date, datetime.date)

    def testCalcMonthMean(self):

        ySmooth = np.ones(365)
        mean = Curve.getMonthMean(ySmooth, 1, 2019)

        self.assertEqual(mean, 1)
