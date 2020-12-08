import wx
from services.DayYearArrayBuildService import DayYearArrayBuildService
from models.Curve import Curve
from models.DataColumn import DataColumn
from panels.PlotPanel import PlotPanel
from wx import lib
from wx.lib import intctrl


class PagePanel(wx.Panel):

    def __init__(self, parent, knmiData):

        super().__init__(parent, -1)

        self.knmiData = knmiData

        # The first and last years of the file are retrieved and put in the GUI as initial year range values.
        self.firstYear = wx.lib.intctrl.IntCtrl(self, size=(50, 20))
        self.firstYear.SetValue(self.knmiData.minYearFile)
        self.lastYear = wx.lib.intctrl.IntCtrl(self, size=(50, 20))
        self.lastYear.SetValue(self.knmiData.maxYearFile)

        # The mouseOver shows the mouseover event text of the plot.
        self.mouseOver = wx.StaticText(self, -1, "Mouse over curve: \n")
        self.mouseOver.SetForegroundColour('#FFFFFF')

        self.plotPanel = PlotPanel(self)
        self.plotPanel.fig.canvas.mpl_connect(
            'motion_notify_event', lambda event: self.plotPanel.onPlotHover(event, self.mouseOver))

        self.errorMessage = wx.StaticText(self, -1, '')
        self.errorMessage.SetForegroundColour('#FF0000')
        self.errorMessage.SetBackgroundColour('#FFFFFF')

    def _plotRawSmooth(self, firstYear: int, lastYear: int,
                       columnName: DataColumn, cla: bool, isDayCurve: bool) -> Curve:

        array = DayYearArrayBuildService.makeArray(self.knmiData.array, firstYear, lastYear, columnName)
        y = array.mean(axis=1 if isDayCurve else 0)
        curve = Curve(y, isDayCurve, firstYear, lastYear)
        self.plotPanel.plot(curve.x, curve.y, curve.ySmooth, cla)

        return curve

    # The pages add the pagepanel controls and texts to their sizer.
    def _addToPage(self, sizer: wx.Sizer):

        sizerGrid = wx.GridSizer(2, 2, 10, 10)
        labelFirstYear = wx.StaticText(self, -1, ' First year: ')
        labelFirstYear.SetForegroundColour('#FFFFFF')
        labelLastYear = wx.StaticText(self, -1, ' Last year: ')
        labelLastYear.SetForegroundColour('#FFFFFF')
        sizerGrid.Add(labelFirstYear)
        sizerGrid.Add(self.firstYear)
        sizerGrid.Add(labelLastYear)
        sizerGrid.Add(self.lastYear)
        sizer.Add(sizerGrid)
        sizer.Add(self.errorMessage)
        sizer.Add(self.plotPanel)
        sizer.Add(self.mouseOver)

        self.SetSizer(sizer)
        self.Layout()

    # When the mouse hovers over the make curve buttons the button text turns black
    # and when the mouse leaves the text is white again.
    @staticmethod
    def _hoverStyleButton(button: wx.Button):

        button.SetForegroundColour('#FFFFFF')
        button.SetBackgroundColour('#00397A')
        button.Bind(wx.EVT_ENTER_WINDOW, lambda event: button.SetForegroundColour('#000000'))
        button.Bind(wx.EVT_LEAVE_WINDOW, lambda event: button.SetForegroundColour('#FFFFFF'))
