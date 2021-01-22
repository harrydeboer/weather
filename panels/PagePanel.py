import wx
from services.DayYearArrayBuildService import DayYearArrayBuildService
from models.Curve import Curve
from models.DataColumn import DataColumn
from panels.PlotPanel import PlotPanel
from wx import lib
from wx.lib import intctrl


class PagePanel(wx.Panel):

    def __init__(self, parent, knmi_data):

        super().__init__(parent, -1)

        self.knmiData = knmi_data

        # The first and last years of the file are retrieved and put in the GUI as initial year range values.
        self.first_year = wx.lib.intctrl.IntCtrl(self, size=(50, 20))
        self.first_year.SetValue(self.knmiData.minYearFile)
        self.last_year = wx.lib.intctrl.IntCtrl(self, size=(50, 20))
        self.last_year.SetValue(self.knmiData.maxYearFile)

        # The mouseOver shows the mouseover event text of the plot.
        self.mouse_over = wx.StaticText(self, -1, "Mouse over curve: \n")
        self.mouse_over.SetForegroundColour('#FFFFFF')

        self.plot_panel = PlotPanel(self)
        self.plot_panel.fig.canvas.mpl_connect(
            'motion_notify_event', lambda event: self.plot_panel.on_plot_hover(event, self.mouse_over))

        self.error_message = wx.StaticText(self, -1, '')
        self.error_message.SetForegroundColour('#FF0000')
        self.error_message.SetBackgroundColour('#FFFFFF')

    def _plot_raw_smooth(self, first_year: int, last_year: int,
                         column_name: DataColumn, cla: bool, is_day_curve: bool) -> Curve:

        array = DayYearArrayBuildService.make_array(self.knmiData.array, first_year, last_year, column_name)
        y = array.mean(axis=1 if is_day_curve else 0)
        curve = Curve(y, is_day_curve, first_year, last_year)
        self.plot_panel.plot(curve.x, curve.y, curve.y_smooth, cla)

        return curve

    # The pages add the pagepanel controls and texts to their sizer.
    def _add_to_page(self, sizer: wx.Sizer):

        sizer_grid = wx.GridSizer(2, 2, 10, 10)
        label_first_year = wx.StaticText(self, -1, ' First year: ')
        label_first_year.SetForegroundColour('#FFFFFF')
        label_last_year = wx.StaticText(self, -1, ' Last year: ')
        label_last_year.SetForegroundColour('#FFFFFF')
        sizer_grid.Add(label_first_year)
        sizer_grid.Add(self.first_year)
        sizer_grid.Add(label_last_year)
        sizer_grid.Add(self.last_year)
        sizer.Add(sizer_grid)
        sizer.Add(self.error_message)
        sizer.Add(self.plot_panel)
        sizer.Add(self.mouse_over)

        self.SetSizer(sizer)
        self.Layout()

    # When the mouse hovers over the make curve buttons the button text turns black
    # and when the mouse leaves the text is white again.
    @staticmethod
    def _hover_style_button(button: wx.Button):

        button.SetForegroundColour('#FFFFFF')
        button.SetBackgroundColour('#00397A')
        button.Bind(wx.EVT_ENTER_WINDOW, lambda event: button.SetForegroundColour('#000000'))
        button.Bind(wx.EVT_LEAVE_WINDOW, lambda event: button.SetForegroundColour('#FFFFFF'))
