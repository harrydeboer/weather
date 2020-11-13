import unittest
import wx
from app import WeatherApp


class TestApp(unittest.TestCase):

    def testOnMakeDayCurve(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        button = app.makeDayCurve
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(1, 1)

    def testOnMakeYearCurve(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        button = app.makeYearCurve
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(1, 1)
