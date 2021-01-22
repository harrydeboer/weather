import unittest
import wx
from app import WeatherApp


class TestTemperaturePanel(unittest.TestCase):

    def testOnMakeDayCurveTemp(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        page = app.page_temperature
        text_output_before = page.text_output.GetLabel()
        button = page.make_day_curve
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(len(page.plot_panel.axes.get_lines()), 6)
        self.assertNotEqual(page.text_output.GetLabel(), text_output_before)

    def testOnMakeYearCurveTemp(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        page = app.page_temperature
        text_output_before = page.text_output.GetLabel()
        button = page.make_year_curve
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(len(page.plot_panel.axes.get_lines()), 2)
        self.assertNotEqual(page.text_output.GetLabel(), text_output_before)
