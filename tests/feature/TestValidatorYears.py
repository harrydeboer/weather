import unittest
import wx
from app import WeatherApp


class TestValidatorYears(unittest.TestCase):

    def testOnPlotHover(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        button = app.page_temperature.make_day_curve
        page = app.page_temperature
        event.SetEventObject(button)

        # Set the first year before the data set and expect an error message.
        page.first_year.SetValue(1900)

        self.assertEqual(page.error_message.GetLabel(), '')

        button.ProcessEvent(event)

        self.assertNotEqual(page.error_message.GetLabel(), '')
