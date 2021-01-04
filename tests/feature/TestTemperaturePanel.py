import unittest
import wx
from app import WeatherApp


class TestTemperaturePanel(unittest.TestCase):

    def testOnMakeDayCurveTemp(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        page = app.pageTemperature
        textOutputBefore = page.textOutput.GetLabel()
        button = page.makeDayCurve
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(len(page.plotPanel.axes.get_lines()), 6)
        self.assertNotEqual(page.textOutput.GetLabel(), textOutputBefore)

    def testOnMakeYearCurveTemp(self):

        app = WeatherApp(False)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        page = app.pageTemperature
        textOutputBefore = page.textOutput.GetLabel()
        button = page.makeYearCurve
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(len(page.plotPanel.axes.get_lines()), 2)
        self.assertNotEqual(page.textOutput.GetLabel(), textOutputBefore)