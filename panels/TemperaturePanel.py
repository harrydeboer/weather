import wx
from panels.PagePanel import PagePanel
from validators.ValidatorFirstYearLastYear import ValidatorFirstYearLastYear
from models.DataColumn import DataColumn


class TemperaturePanel(PagePanel):

    def __init__(self, parent, knmiData):

        super().__init__(parent, knmiData)

        # The textOutput shows the first day of summer or the temperature increase.
        self.textOutput = wx.StaticText(self, -1, '')
        self.textOutput.SetForegroundColour('#FFFFFF')

        # The makeDayCurve and makeYearCurve button click events are bound to callbacks and validators.
        self.makeDayCurve = wx.Button(self, label='make day curve')
        self.makeDayCurve.Bind(wx.EVT_BUTTON, self.OnMakeDayCurveTemp)
        self.makeDayCurve.SetValidator(
            ValidatorFirstYearLastYear('dayCurve', self.firstYear, self.lastYear, self.errorMessage))
        self.makeYearCurve = wx.Button(self, label="make year curve")
        self.makeYearCurve.Bind(wx.EVT_BUTTON, self.OnMakeYearCurveTemp)
        self.makeYearCurve.SetValidator(
            ValidatorFirstYearLastYear('yearCurve', self.firstYear, self.lastYear, self.errorMessage))

        self._hoverStyleButton(self.makeDayCurve)
        self._hoverStyleButton(self.makeYearCurve)

        sizerV = wx.BoxSizer(wx.VERTICAL)
        sizerH = wx.BoxSizer(wx.HORIZONTAL)
        sizerH.Add(self.makeDayCurve)
        sizerH.Add(self.makeYearCurve)
        sizerV.Add(sizerH)
        sizerV.Add(self.textOutput)

        self._addToPage(sizerV)

    def OnMakeDayCurveTemp(self, _):

        firstYear = self.firstYear.GetValue()
        lastYear = self.lastYear.GetValue()

        self._plotRawSmooth(firstYear, lastYear, DataColumn.minTemp, True, True)
        curve = self._plotRawSmooth(firstYear, lastYear, DataColumn.meanTemp, False, True)
        self._plotRawSmooth(firstYear, lastYear, DataColumn.maxTemp, False, True)

        self.textOutput.SetLabel('First day of summer: ' + curve.getFirstDateSummer().strftime("%d %B") + '.')

    def OnMakeYearCurveTemp(self, _):

        curve = self._plotRawSmooth(self.firstYear.GetValue(), self.lastYear.GetValue(),
                                    DataColumn.meanTemp, True, False)

        self.textOutput.SetLabel('Temperature increase: ' +
                                 str(int((curve.ySmooth[-1] - curve.ySmooth[0]) * 10) / 10) + "°.")
