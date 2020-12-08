import wx
from panels.PagePanel import PagePanel
from models.DataColumn import DataColumn
from validators.ValidatorFirstYearLastYear import ValidatorFirstYearLastYear


class RainPanel(PagePanel):

    def __init__(self, parent, knmiData):

        super().__init__(parent, knmiData)

        # The makeDayCurveAmount and makeDayCurvePercentage button click events are bound to callbacks and validators.
        self.makeDayCurveAmount = wx.Button(self, label='make day curve amount')
        self.makeDayCurveAmount.Bind(wx.EVT_BUTTON, self.OnMakeDayCurve)
        self.makeDayCurveAmount.SetValidator(
            ValidatorFirstYearLastYear('dayCurve', self.firstYear, self.lastYear, self.errorMessage))
        self.makeDayCurvePercentage = wx.Button(self, label='make day curve percentage')
        self.makeDayCurvePercentage.Bind(wx.EVT_BUTTON, self.OnMakeDayCurvePercentage)
        self.makeDayCurvePercentage.SetValidator(
            ValidatorFirstYearLastYear('rainPercentage', self.firstYear, self.lastYear, self.errorMessage))

        self._hoverStyleButton(self.makeDayCurveAmount)
        self._hoverStyleButton(self.makeDayCurvePercentage)

        sizerV = wx.BoxSizer(wx.VERTICAL)
        sizerH = wx.BoxSizer(wx.HORIZONTAL)
        sizerH.Add(self.makeDayCurveAmount)
        sizerH.Add(self.makeDayCurvePercentage)
        sizerV.Add(sizerH)

        self._addToPage(sizerV)

    def OnMakeDayCurve(self, _):

        self._plotRawSmooth(self.firstYear.GetValue(), self.lastYear.GetValue(), DataColumn.amountRain, True, True)

    def OnMakeDayCurvePercentage(self, _):

        self._plotRawSmooth(self.firstYear.GetValue(), self.lastYear.GetValue(), DataColumn.percRain, True, True)
