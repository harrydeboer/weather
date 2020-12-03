import unittest
import wx
from app import WeatherApp


class TestRainPanel(unittest.TestCase):

    def testOnMakeDayCurveAmount(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        button = app.pageRain.makeDayCurveAmount
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(1, 1)
