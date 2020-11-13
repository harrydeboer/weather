import unittest
import wx
from app import WeatherApp


class TestPlotPanel(unittest.TestCase):

    def testOnPlotHover(self):

        # Fill the app with curves. The app needs to be visible.
        app = WeatherApp(True)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        button = app.makeDayCurve
        event.SetEventObject(button)
        button.ProcessEvent(event)

        # Make an mouse over event and process the event.
        canvas = app.plotPanel.fig.canvas
        canvas.motion_notify_event(272, 313) # xdata 173.72 ydata 20.86

        self.assertEqual(1, 1)
