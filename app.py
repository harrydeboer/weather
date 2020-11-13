import wx
import wx.xrc as xrc
from panels.PlotPanel import PlotPanel
from models.CsvReader import CsvReader
from models.DayYearArrayBuilder import DayYearArrayBuilder
from models.Curve import Curve
from models.DataColumn import DataColumn
import locale


class WeatherApp(wx.App):

    def __init__(self, isShown: bool):

        super().__init__()

        # The locale is en_GB to set the language on english.
        locale.setlocale(locale.LC_ALL, 'en_GB')

        self.res = xrc.XmlResource('layout/weather.xml')
        self.mainFrame = self.res.LoadFrame(None, "mainFrame")
        self.mainPanel = xrc.XRCCTRL(self.mainFrame, "mainPanel")

        # The data is read.
        # The first and last years of the file are retrieved and put in the GUI as initial range values.
        self.csvReader = CsvReader()
        self.firstYearInput = xrc.XRCCTRL(self.mainFrame, "firstYear")
        self.firstYearInput.SetValue(self.csvReader.minYearFile)
        self.lastYearInput = xrc.XRCCTRL(self.mainFrame, "lastYear")
        self.lastYearInput.SetValue(self.csvReader.maxYearFile)

        plotContainerPanel = xrc.XRCCTRL(self.mainFrame, "plotContainerPanel")
        sizer = wx.BoxSizer(wx.VERTICAL)

        # The DateTemp shows the first day of summer or the temperature increase.
        self.tempOfDate = xrc.XRCCTRL(self.mainFrame, 'tempOfDate')

        # The TextOutput shows the mouseover event of the plot.
        self.textOutput = xrc.XRCCTRL(self.mainFrame, 'textOutput')
        self.plotPanel = PlotPanel(plotContainerPanel)
        self.plotPanel.fig.canvas.mpl_connect('motion_notify_event',
                                              lambda event: self.plotPanel.onPlotHover(event, self.tempOfDate))
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
    def __validateYearRange(self, curveType: str):

        firstYear = self.firstYearInput.GetValue()
        lastYear = self.lastYearInput.GetValue()

        if not firstYear.isdigit() or not lastYear.isdigit():
            self.textOutput.SetForegroundColour((255, 0, 0))
            text = 'Year range input cannot be empty, text or negative.'
            self.textOutput.SetLabel(text)

            raise Exception(text)

        firstYear, lastYear = int(firstYear), int(lastYear)
        if lastYear < firstYear:
            self.textOutput.SetForegroundColour((255, 0, 0))
            text = 'Last year cannot be smaller than first year.'
            self.textOutput.SetLabel(text)

            raise Exception(text)

        if firstYear < int(self.csvReader.minYearFile) or lastYear > int(self.csvReader.maxYearFile):
            self.textOutput.SetForegroundColour((255, 0, 0))
            text = 'Years out of range ' + self.csvReader.minYearFile + '-' + self.csvReader.maxYearFile + '.'
            self.textOutput.SetLabel(text)

            raise Exception(text)

        if curveType == 'yearCurve' and lastYear - firstYear < 5 - 1:
            self.textOutput.SetForegroundColour((255, 0, 0))
            text = 'Range should be 5 years at least.'
            self.textOutput.SetLabel(text)

            raise Exception(text)

        self.textOutput.SetForegroundColour((255, 255, 255))

        return firstYear, lastYear

    def __plotRawSmooth(self, firstYear: int, lastYear: int, columnName: DataColumn, cla: bool, meanAxis: int):

        tempArray = DayYearArrayBuilder.makeArray(self.csvReader.csvArray, firstYear, lastYear, columnName)
        curve = Curve(tempArray, meanAxis, firstYear, lastYear)
        self.plotPanel.plot(curve.x, curve.y, curve.ySmooth, cla)

        return curve


if __name__ == '__main__':
    app = WeatherApp(True)
    app.MainLoop()
