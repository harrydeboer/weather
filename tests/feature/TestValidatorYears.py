import unittest
import wx
from app import WeatherApp


class TestValidatorYears(unittest.TestCase):

    def testOnPlotHover(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        button = app.pageTemperature.makeDayCurve
        page = app.pageTemperature
        event.SetEventObject(button)

        # Set the first year before the data set and expect an error message.
        page.firstYear.SetValue(1900)

        self.assertEqual(page.errorMessage.GetLabel(), '')

        button.ProcessEvent(event)

        self.assertNotEqual(page.errorMessage.GetLabel(), '')
