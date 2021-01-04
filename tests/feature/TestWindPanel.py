import unittest
import wx
from app import WeatherApp


class TestWindPanel(unittest.TestCase):

    def testOnMakeDayCurveSpeed(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        page = app.pageWind
        button = page.makeDayCurveSpeed
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(len(page.plotPanel.axes.get_lines()), 2)

    def testOnDayMakeCurveDirection(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        page = app.pageWind
        button = page.makeDayCurveDirection
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(len(page.plotPanel.axes.get_lines()), 2)
