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
        width, height = page.plotPanel.canvas.get_width_height()
        curve = page.plotPanel.axes.get_lines()[1]
        curve.set_pickradius(1)

        for itemx in range(width):
            for itemy in range(height):
                mouseEvent = MouseEvent('motion_notify_event', page.plotPanel.canvas, x=itemx, y=itemy)
                if curve.contains(mouseEvent)[0]:
                    break
            else:
                continue

            break

        # Make an mouse over event and process the event.
        app.pageTemperature.plotPanel.onPlotHover(mouseEvent, page.mouseOver)
        self.assertNotEqual(page.mouseOver.GetLabel(), 'Mouse over curve: \n')
