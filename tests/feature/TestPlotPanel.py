import unittest
import wx
from app import WeatherApp
from matplotlib.backend_bases import MouseEvent


class TestPlotPanel(unittest.TestCase):

    def testOnPlotHover(self):

        # Fill the temperature plotpanel with curves. The app needs to be visible.
        app = WeatherApp(True)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        button = app.pageTemperature.makeDayCurve
        page = app.pageTemperature
        event.SetEventObject(button)
        button.ProcessEvent(event)

        self.assertEqual(app.pageTemperature.mouseOver.GetLabel(), 'Mouse over curve: \n')
        xdata = 157.94
        ydata = 19.704

        # Make an mouse over event and process the event.
        mouseEvent = MouseEvent('motion_notify_event', page.plotPanel.canvas, x=174, y=227)
        app.pageTemperature.plotPanel.onPlotHover(mouseEvent, page.mouseOver)
        self.assertNotEqual(page.mouseOver.GetLabel(), 'Mouse over curve: \n')
