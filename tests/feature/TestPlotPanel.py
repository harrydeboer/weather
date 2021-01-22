import unittest
import wx
from app import WeatherApp
from matplotlib.backend_bases import MouseEvent


class TestPlotPanel(unittest.TestCase):

    def testOnPlotHover(self):

        # Fill the temperature plotpanel with curves. The app needs to be visible.
        app = WeatherApp(True)
        event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK)
        button = app.page_temperature.make_day_curve
        page = app.page_temperature
        event.SetEventObject(button)
        button.ProcessEvent(event)

        mouse_over_before = app.page_temperature.mouse_over.GetLabel()
        width, height = page.plot_panel.canvas.get_width_height()
        curve = page.plot_panel.axes.get_lines()[1]
        curve.set_pickradius(1)

        mouse_event = None
        for itemx in range(width):
            for itemy in range(height):
                mouse_event = MouseEvent('motion_notify_event', page.plot_panel.canvas, x=itemx, y=itemy)
                if curve.contains(mouse_event)[0]:
                    break
            else:
                continue

            break

        page.plot_panel.canvas.motion_notify_event(mouse_event.x, mouse_event.y)

        self.assertNotEqual(page.mouse_over.GetLabel(), mouse_over_before)
