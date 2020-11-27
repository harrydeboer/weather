import wx
import wx.xrc as xrc
from typing import Tuple
from services.DateArrayBuildService import DateArrayBuildService
from models.Curve import Curve
from models.DataColumn import DataColumn
from panels.PlotPanel import PlotPanel


class PagePanel(wx.Panel):

    def __init__(self, parent, knmiData):

        wx.Panel.__init__(self, parent, -1)

        self.knmiData = knmiData

        # The first and last years of the file are retrieved and put in the GUI as initial year range values.
        self.firstYearInput = xrc.XRCCTRL(parent, "firstYear")
        self.firstYearInput.SetValue(self.knmiData.minYearFile)
        self.lastYearInput = xrc.XRCCTRL(parent, "lastYear")
        self.lastYearInput.SetValue(self.knmiData.maxYearFile)

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

    # The user values from the first and last year text controls is validated.
    def _validateYearRange(self, curveType: str, page: str) -> Tuple[int, int]:

        if page == 'temperature':
            firstYear = self.firstYearInput.GetValue()
            lastYear = self.lastYearInput.GetValue()
            errorMessage = self.errorMessage
        elif page == 'wind':
            firstYear = self.firstYearInput.GetValue()
            lastYear = self.lastYearInput.GetValue()
            errorMessage = self.errorMessage
        else:
            raise Exception('Page must be either temperature or wind.')

        if not firstYear.isdigit() or not lastYear.isdigit():
            text = 'Year range input cannot be empty, text or negative.'
            errorMessage.SetLabel(text)

            raise Exception(text)

        firstYear, lastYear = int(firstYear), int(lastYear)
        if lastYear < firstYear:
            text = 'Last year cannot be smaller than first year.'
            errorMessage.SetLabel(text)

            raise Exception(text)

        if firstYear < int(self.knmiData.minYearFile) or lastYear > int(self.knmiData.maxYearFile):
            text = 'Years out of range ' + self.knmiData.minYearFile + '-' + self.knmiData.maxYearFile + '.'
            errorMessage.SetLabel(text)

            raise Exception(text)

        if curveType == 'yearCurve' and lastYear - firstYear < 5 - 1:
            text = 'Range should be 5 years at least.'
            errorMessage.SetLabel(text)

            raise Exception(text)

        errorMessage.SetLabel('')

        return firstYear, lastYear

    def _plotRawSmooth(self, firstYear: int, lastYear: int,
                       columnName: DataColumn, cla: bool, isDayCurve: bool) -> Curve:

        array = DateArrayBuildService.makeArray(self.knmiData.array, firstYear, lastYear, columnName)
        y = array.mean(axis=1 if isDayCurve else 0)
        curve = Curve(y, isDayCurve, firstYear, lastYear)
        self.plotPanel.plot(curve.x, curve.y, curve.ySmooth, cla)

        return curve
