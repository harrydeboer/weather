import unittest
import wx
from app import WeatherApp


class TestApp(unittest.TestCase):

    def testOnMakeDayCurveTemp(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        button = app.pageTemperature.makeDayCurve
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(1, 1)

    def testOnMakeYearCurveTemp(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        button = app.pageTemperature.makeYearCurve
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(1, 1)

    def testOnMakeDayCurveSpeed(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        button = app.pageWind.makeDayCurveSpeed
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(1, 1)

    def testOnDayMakeCurveDirection(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        button = app.pageWind.makeDayCurveDirection
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(1, 1)
