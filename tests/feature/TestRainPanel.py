import unittest
import wx
from app import WeatherApp


class TestRainPanel(unittest.TestCase):

    def testOnMakeDayCurveAmount(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        page = app.pageRain
        button = page.makeDayCurveAmount
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(len(page.plotPanel.axes.get_lines()), 2)

    def testOnMakeDayCurvePercentage(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        page = app.pageRain
        page.firstYear.SetValue(1930)
        button = page.makeDayCurvePercentage
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(len(page.plotPanel.axes.get_lines()), 2)
