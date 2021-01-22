import unittest
import numpy as np
import datetime as datetime
from services.DayYearArrayBuildService import DayYearArrayBuildService
from models.KNMIData import KNMIData
from models.Curve import Curve
from models.DataColumn import DataColumn


class TestCurve(unittest.TestCase):

    def setUp(self):

        self.first_year = 1906
        self.last_year = 2019
        self.knmi_data = KNMIData()
        temp_array = DayYearArrayBuildService.make_array(self.knmi_data.array,
                                                         self.first_year, self.last_year, DataColumn.mean_temp)
        self.curve = Curve(temp_array.mean(axis=1), True, self.first_year, self.last_year)
        self.curve_lin_extrapolate = Curve(temp_array.mean(axis=0), False, self.first_year, self.last_year)

    def testSmoothCurve(self):

        self.assertEqual(self.curve.y_smooth.size, 365)

    def testSmoothCurveLinExtrapolate(self):

        self.assertEqual(self.curve_lin_extrapolate.y_smooth.size, self.last_year - self.first_year + 1)

    def testFirstDateSummer(self):

        date = self.curve.get_first_date_summer()

        self.assertIsInstance(date, datetime.date)

    def testCalcMonthMean(self):

        y_smooth = np.ones(365)
        mean = Curve.get_month_mean(y_smooth, 1, 2019)

        self.assertEqual(mean, 1)

    def testMeanOfAngle(self):

        first_year = 1906
        last_year = 2019
        speed_2d = DayYearArrayBuildService.make_array(self.knmi_data.array, first_year,
                                                       last_year, DataColumn.wind_speed_va)
        angle_2d = DayYearArrayBuildService.make_array(self.knmi_data.array, first_year,
                                                       last_year, DataColumn.wind_direction)
        angle = self.curve.mean_of_angle(speed_2d, angle_2d)

        self.assertEqual(angle.size, 365)
