import wx
from panels.PagePanel import PagePanel
from models.DataColumn import DataColumn
from validators.ValidatorFirstYearLastYear import ValidatorFirstYearLastYear


class SunshinePanel(PagePanel):

    def __init__(self, parent, knmiData):

        super().__init__(parent, knmiData)

        # The makeDayCurve button click event is bound to a callback and a validator.
        self.makeDayCurve = wx.Button(self, label='make day curve')
        self.makeDayCurve.Bind(wx.EVT_BUTTON, self.OnMakeDayCurve)
        self.makeDayCurve.SetValidator(
            ValidatorFirstYearLastYear('dayCurve', self.firstYear, self.lastYear, self.errorMessage))

        self._hoverStyleButton(self.makeDayCurve)

        sizerV = wx.BoxSizer(wx.VERTICAL)
        sizerV.Add(self.makeDayCurve)

        self._addToPage(sizerV)

    def OnMakeDayCurve(self, _):

        self._plotRawSmooth(self.firstYear.GetValue(), self.lastYear.GetValue(), DataColumn.percSunshine, True, True)
