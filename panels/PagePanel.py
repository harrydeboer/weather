import wx
import wx.xrc as xrc
from wx.core import StaticText
from services.DateArrayBuildService import DateArrayBuildService
from models.Curve import Curve
from models.DataColumn import DataColumn
from panels.PlotPanel import PlotPanel
from validators.ValidatorIntTextCtrl import ValidatorIntTextCtrl


class PagePanel(wx.Panel):

    def __init__(self, parent, knmiData):

        wx.Panel.__init__(self, parent, -1)

        self.knmiData = knmiData

        # The first and last years of the file are retrieved and put in the GUI as initial year range values.
        self.firstYear = xrc.XRCCTRL(parent, "firstYear")
        self.firstYear.SetValue(self.knmiData.minYearFile)
        self.firstYear.SetValidator(ValidatorIntTextCtrl())
        self.lastYear = xrc.XRCCTRL(parent, "lastYear")
        self.lastYear.SetValue(self.knmiData.maxYearFile)
        self.lastYear.SetValidator(ValidatorIntTextCtrl())

        # The mouseOver shows the mouseover event text of the plot.
        self.mouseOver = xrc.XRCCTRL(parent, 'mouseOver')

        sizer = wx.BoxSizer(wx.VERTICAL)
        plotContainerPanel = xrc.XRCCTRL(parent, "plotContainerPanel")
        self.plotPanel = PlotPanel(plotContainerPanel)
        self.plotPanel.fig.canvas.mpl_connect(
            'motion_notify_event', lambda event: self.plotPanel.onPlotHover(event, self.mouseOver))

        sizer.Add(self.plotPanel, 1, wx.EXPAND)
        plotContainerPanel.SetSizer(sizer)

        self.errorMessage = xrc.XRCCTRL(parent, 'errorMessage')

    def _plotRawSmooth(self, firstYear: int, lastYear: int,
                       columnName: DataColumn, cla: bool, isDayCurve: bool) -> Curve:

        array = DateArrayBuildService.makeArray(self.knmiData.array, firstYear, lastYear, columnName)
        y = array.mean(axis=1 if isDayCurve else 0)
        curve = Curve(y, isDayCurve, firstYear, lastYear)
        self.plotPanel.plot(curve.x, curve.y, curve.ySmooth, cla)

        return curve

    # When the mouse hovers over the make curve buttons the button text turns black
    # and when the mouse leaves the text is white again.
    @staticmethod
    def _hoverStyleButton(button: StaticText):

        button.Bind(wx.EVT_ENTER_WINDOW, lambda event: button.SetForegroundColour('#000000'))
        button.Bind(wx.EVT_LEAVE_WINDOW, lambda event: button.SetForegroundColour('#FFFFFF'))
