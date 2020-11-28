import unittest
import numpy as np
import datetime as datetime
from services.DateArrayBuildService import DateArrayBuildService
from models.KNMIData import KNMIData
from models.Curve import Curve


class TestCurve(unittest.TestCase):

    def setUp(self):

        self.firstYear = 1904
        self.lastYear = 2019
        self.knmiData = KNMIData()
        tempArray = DateArrayBuildService.makeArray(self.knmiData.array, self.firstYear, self.lastYear, 'meanTemp')
        self.curve = Curve(tempArray.mean(axis=1), True, self.firstYear, self.lastYear)

    def testSmoothCurve(self):

        self.assertEqual(self.curve.ySmooth.size, 365)

    def testFirstDateSummer(self):

        date = self.curve.getFirstDateSummer()

        self.assertIsInstance(date, datetime.date)

    def testCalcMonthMean(self):

        ySmooth = np.ones(365)
        mean = Curve.getMonthMean(ySmooth, 1, 2019)

        self.assertEqual(mean, 1)

    def testMeanOfAngle(self):

        firstYear = 1904
        lastYear = 2019
        speed2D = DateArrayBuildService.makeArray(self.knmiData.array, firstYear, lastYear, 'windSpeedVA')
        angle2D = DateArrayBuildService.makeArray(self.knmiData.array, firstYear, lastYear, 'windDirection')
        angle = self.curve.meanOfAngle(speed2D, angle2D)

        self.assertEqual(angle.size, 365)
