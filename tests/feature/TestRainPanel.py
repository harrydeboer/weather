import unittest
import wx
from app import WeatherApp


class TestRainPanel(unittest.TestCase):

    def testOnMakeDayCurveAmount(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        page = app.page_rain
        button = page.make_day_curve_amount
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(len(page.plot_panel.axes.get_lines()), 2)

    def testOnMakeDayCurvePercentage(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        page = app.page_rain
        page.first_year.SetValue(1930)
        button = page.make_day_curve_percentage
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(len(page.plot_panel.axes.get_lines()), 2)
