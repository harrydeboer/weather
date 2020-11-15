import wx
import wx.xrc as xrc
from panels.PlotPanel import PlotPanel
from models.KNMIData import KNMIData
from models.DayYearArrayBuilder import DayYearArrayBuilder
from models.Curve import Curve
from models.DataColumn import DataColumn
from typing import Tuple
import locale


class WeatherApp(wx.App):

    def __init__(self, isShown: bool):

        super().__init__()

        # The locale is en_GB to set the language on english.
        locale.setlocale(locale.LC_ALL, 'en_GB')

        self.res = xrc.XmlResource('layout/weather.xml')
        self.mainFrame = self.res.LoadFrame(None, "mainFrame")
        self.mainPanel = xrc.XRCCTRL(self.mainFrame, "mainPanel")

        # The data is read by instantiating the KNMIData class.
        # The first and last years of the file are retrieved and put in the GUI as initial year range values.
        self.knmiData = KNMIData()
        self.firstYearInput = xrc.XRCCTRL(self.mainFrame, "firstYear")
        self.firstYearInput.SetValue(self.knmiData.minYearFile)
        self.lastYearInput = xrc.XRCCTRL(self.mainFrame, "lastYear")
        self.lastYearInput.SetValue(self.knmiData.maxYearFile)

        plotContainerPanel = xrc.XRCCTRL(self.mainFrame, "plotContainerPanel")
        sizer = wx.BoxSizer(wx.VERTICAL)

        # The textOutput shows the first day of summer or the temperature increase.
        self.textOutput = xrc.XRCCTRL(self.mainFrame, 'textOutput')

        # The mouseOver shows the mouse over event text.
        self.errorMessage = xrc.XRCCTRL(self.mainFrame, 'errorMessage')

        # The mouseOver shows the mouseover event text of the plot.
        self.mouseOver = xrc.XRCCTRL(self.mainFrame, 'mouseOver')
        self.plotPanel = PlotPanel(plotContainerPanel)
        self.plotPanel.fig.canvas.mpl_connect('motion_notify_event',
                                              lambda event: self.plotPanel.onPlotHover(event, self.mouseOver))
        sizer.Add(self.plotPanel, 1, wx.EXPAND)
        plotContainerPanel.SetSizer(sizer)

        # The show_day_curve and show_year_curve button click events are bound to OnShowDayCurve and OnShowYearCurve.
        self.makeDayCurve = xrc.XRCCTRL(self.mainFrame, "makeDayCurve")
        self.makeDayCurve.Bind(wx.EVT_BUTTON, self.OnMakeDayCurve)
        self.makeYearCurve = xrc.XRCCTRL(self.mainFrame, "makeYearCurve")
        self.makeYearCurve.Bind(wx.EVT_BUTTON, self.OnMakeYearCurve)

        # When the mouse hovers over the show_day_curve and show_year_curve buttons the button text turns black
        # and when the mouse leaves the text is white again.
        self.makeDayCurve.Bind(wx.EVT_ENTER_WINDOW, lambda event: self.makeDayCurve.SetForegroundColour('#000000'))
        self.makeDayCurve.Bind(wx.EVT_LEAVE_WINDOW, lambda event: self.makeDayCurve.SetForegroundColour('#FFFFFF'))
        self.makeYearCurve.Bind(wx.EVT_ENTER_WINDOW, lambda event: self.makeYearCurve.SetForegroundColour('#000000'))
        self.makeYearCurve.Bind(wx.EVT_LEAVE_WINDOW, lambda event: self.makeYearCurve.SetForegroundColour('#FFFFFF'))

        self.mainFrame.Show(isShown)

        self.SetTopWindow(self.mainFrame)

    def OnMakeDayCurve(self, _):

        firstYear, lastYear = self.__validateYearRange('dayCurve')
        self.__plotRawSmooth(firstYear, lastYear, 'minTemp', True, 1)
        curve = self.__plotRawSmooth(firstYear, lastYear, 'meanTemp', False, 1)
        firstDate = curve.getFirstDateSummer()
        self.__plotRawSmooth(firstYear, lastYear, 'maxTemp', False, 1)
        self.textOutput.SetLabel('First day of summer: ' + firstDate.strftime("%d %B") + '.')

    def OnMakeYearCurve(self, _):

        firstYear, lastYear = self.__validateYearRange('yearCurve')
        curve = self.__plotRawSmooth(firstYear, lastYear, 'meanTemp', True, 0)
        self.textOutput.SetLabel('Temperature increase: ' +
                                 str(int((curve.ySmooth[-1] - curve.ySmooth[0]) * 10) / 10) + "°.")

        # The user values from the first and last year text controls is validated.
    def __validateYearRange(self, curveType: str) -> Tuple[int, int]:

        firstYear = self.firstYearInput.GetValue()
        lastYear = self.lastYearInput.GetValue()

        if not firstYear.isdigit() or not lastYear.isdigit():
            text = 'Year range input cannot be empty, text or negative.'
            self.errorMessage.SetLabel(text)

            raise Exception(text)

        firstYear, lastYear = int(firstYear), int(lastYear)
        if lastYear < firstYear:
            text = 'Last year cannot be smaller than first year.'
            self.errorMessage.SetLabel(text)

            raise Exception(text)

        if firstYear < int(self.knmiData.minYearFile) or lastYear > int(self.knmiData.maxYearFile):
            text = 'Years out of range ' + self.knmiData.minYearFile + '-' + self.knmiData.maxYearFile + '.'
            self.errorMessage.SetLabel(text)

            raise Exception(text)

        if curveType == 'yearCurve' and lastYear - firstYear < 5 - 1:
            text = 'Range should be 5 years at least.'
            self.errorMessage.SetLabel(text)

            raise Exception(text)

        self.errorMessage.SetLabel('')

        return firstYear, lastYear

    def __plotRawSmooth(self, firstYear: int, lastYear: int, columnName: DataColumn, cla: bool, meanAxis: int) -> Curve:

        tempArray = DayYearArrayBuilder.makeArray(self.knmiData.array, firstYear, lastYear, columnName)
        curve = Curve(tempArray, meanAxis, firstYear, lastYear)
        self.plotPanel.plot(curve.x, curve.y, curve.ySmooth, cla)

        return curve


if __name__ == '__main__':
    app = WeatherApp(True)
    app.MainLoop()
