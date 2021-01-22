import unittest
import wx
from app import WeatherApp


class TestWindPanel(unittest.TestCase):

    def testOnMakeDayCurveSpeed(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        page = app.page_wind
        button = page.make_day_curve_speed
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(len(page.plot_panel.axes.get_lines()), 2)

    def testOnDayMakeCurveDirection(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        page = app.page_wind
        button = page.make_day_curve_direction
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(len(page.plot_panel.axes.get_lines()), 2)
