import unittest
import wx
from app import WeatherApp


class TestSunshinePanel(unittest.TestCase):

    def testOnMakeDayCurve(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        page = app.page_sunshine
        button = page.make_day_curve_percentage
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(len(page.plot_panel.axes.get_lines()), 2)
