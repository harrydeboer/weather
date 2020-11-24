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
        self.mainFrame = self.res.LoadFrame(None, 'mainFrame')
        self.mainPanel = xrc.XRCCTRL(self.mainFrame, 'mainPanel')

        sizer = wx.BoxSizer()
        self.notebook = wx.Notebook(self.mainPanel)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.mainPanel.SetSizer(sizer)
        self.mainPanel.Layout()
        self.pageTemperature = self.res.LoadPanel(self.notebook, 'temperature')
        self.pageWind = self.res.LoadPanel(self.notebook, 'wind')
        self.notebook.AddPage(self.pageTemperature, 'Temperature', True)
        self.notebook.AddPage(self.pageWind, 'Wind', True)
        self.notebook.ChangeSelection(0)

        # The data is read by instantiating the KNMIData class.
        # The first and last years of the file are retrieved and put in the GUI as initial year range values.
        self.knmiData = KNMIData()
        self.firstYearInputTemp = xrc.XRCCTRL(self.pageTemperature, "firstYear")
        self.firstYearInputTemp.SetValue(self.knmiData.minYearFile)
        self.lastYearInputTemp = xrc.XRCCTRL(self.pageTemperature, "lastYear")
        self.lastYearInputTemp.SetValue(self.knmiData.maxYearFile)
        self.firstYearInputWind = xrc.XRCCTRL(self.pageWind, "firstYear")
        self.firstYearInputWind.SetValue(self.knmiData.minYearFile)
        self.lastYearInputWind = xrc.XRCCTRL(self.pageWind, "lastYear")
        self.lastYearInputWind.SetValue(self.knmiData.maxYearFile)

        plotContainerPanelTemp = xrc.XRCCTRL(self.pageTemperature, "plotContainerPanel")
        plotContainerPanelWind = xrc.XRCCTRL(self.pageWind, "plotContainerPanel")
        sizer = wx.BoxSizer(wx.VERTICAL)

        # The textOutput shows the first day of summer or the temperature increase.
        self.textOutput = xrc.XRCCTRL(self.pageTemperature, 'textOutput')

        # The mouseOver shows the mouse over event text.
        self.errorMessage = xrc.XRCCTRL(self.pageTemperature, 'errorMessage')

        # The mouseOver shows the mouseover event text of the plot.
        self.mouseOver = xrc.XRCCTRL(self.pageTemperature, 'mouseOver')
        self.plotPanelTemp = PlotPanel(plotContainerPanelTemp)
        self.plotPanelWind = PlotPanel(plotContainerPanelWind)
        self.plotPanelTemp.fig.canvas.mpl_connect('motion_notify_event',
                                              lambda event: self.plotPanelTemp.onPlotHover(event, self.mouseOver))
        sizer.Add(self.plotPanelTemp, 1, wx.EXPAND)
        sizer.Add(self.plotPanelWind, 1, wx.EXPAND)
        plotContainerPanelTemp.SetSizer(sizer)
        plotContainerPanelWind.SetSizer(sizer)

        # The makeDayCurve and makeYearCurve button click events are bound to callbacks.
        self.makeDayCurveTemp = xrc.XRCCTRL(self.pageTemperature, "makeDayCurve")
        self.makeDayCurveTemp.Bind(wx.EVT_BUTTON, self.OnMakeDayCurveTemp)
        self.makeDayCurveWind = xrc.XRCCTRL(self.pageWind, "makeDayCurve")
        self.makeDayCurveWind.Bind(wx.EVT_BUTTON, self.OnMakeDayCurveWind)
        self.makeYearCurveTemp = xrc.XRCCTRL(self.pageTemperature, "makeYearCurve")
        self.makeYearCurveTemp.Bind(wx.EVT_BUTTON, self.OnMakeYearCurveTemp)

        # When the mouse hovers over the show_day_curve and show_year_curve buttons the button text turns black
        # and when the mouse leaves the text is white again.
        self.makeDayCurveTemp.Bind(wx.EVT_ENTER_WINDOW, lambda event: self.makeDayCurveTemp.SetForegroundColour('#000000'))
        self.makeDayCurveTemp.Bind(wx.EVT_LEAVE_WINDOW, lambda event: self.makeDayCurveTemp.SetForegroundColour('#FFFFFF'))
        self.makeYearCurveTemp.Bind(wx.EVT_ENTER_WINDOW, lambda event: self.makeYearCurveTemp.SetForegroundColour('#000000'))
        self.makeYearCurveTemp.Bind(wx.EVT_LEAVE_WINDOW, lambda event: self.makeYearCurveTemp.SetForegroundColour('#FFFFFF'))

        self.mainFrame.Show(isShown)

        self.SetTopWindow(self.mainFrame)

    def OnMakeDayCurveTemp(self, _):

        firstYear, lastYear = self.__validateYearRange('dayCurve', 'temperature')
        self.__plotRawSmooth(firstYear, lastYear, 'minTemp', True, 1)
        curve = self.__plotRawSmooth(firstYear, lastYear, 'meanTemp', False, 1)
        firstDate = curve.getFirstDateSummer()
        self.__plotRawSmooth(firstYear, lastYear, 'maxTemp', False, 1)
        self.textOutput.SetLabel('First day of summer: ' + firstDate.strftime("%d %B") + '.')

    def OnMakeDayCurveWind(self, _):

        firstYear, lastYear = self.__validateYearRange('dayCurve', 'wind')
        self.__plotRawSmooth(firstYear, lastYear, 'windSpeed', True, 1)

    def OnMakeYearCurveTemp(self, _):

        firstYear, lastYear = self.__validateYearRange('yearCurve', 'temperature')
        curve = self.__plotRawSmooth(firstYear, lastYear, 'meanTemp', True, 0)
        self.textOutput.SetLabel('Temperature increase: ' +
                                 str(int((curve.ySmooth[-1] - curve.ySmooth[0]) * 10) / 10) + "°.")

        # The user values from the first and last year text controls is validated.
    def __validateYearRange(self, curveType: str, page: str) -> Tuple[int, int]:

        if page == 'temperature':
            firstYear = self.firstYearInputTemp.GetValue()
            lastYear = self.lastYearInputTemp.GetValue()
        elif page == 'wind':
            firstYear = self.firstYearInputWind.GetValue()
            lastYear = self.lastYearInputWind.GetValue()
        else:
            raise Exception('Page must be either temperature or wind.')

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
        if columnName == 'windSpeed':
            self.plotPanelWind.plot(curve.x, curve.y, curve.ySmooth, cla)
        else:
           self.plotPanelTemp.plot(curve.x, curve.y, curve.ySmooth, cla)

        return curve


if __name__ == '__main__':
    app = WeatherApp(True)
    app.MainLoop()
