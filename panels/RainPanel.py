import wx
import wx.xrc as xrc
from panels.PagePanel import PagePanel
from models.DataColumn import DataColumn
from validators.ValidatorYears import ValidatorYears


class RainPanel(PagePanel):

    def __init__(self, parent, knmiData):

        super().__init__(parent, knmiData)

        # The makeDayCurveSpeed and makeDayCurveDirection button click events are bound to callbacks.
        self.makeDayCurveAmount = xrc.XRCCTRL(parent, "makeDayCurveAmount")
        self.makeDayCurveAmount.Bind(wx.EVT_BUTTON, self.OnMakeDayCurve)
        self.makeDayCurveAmount.SetValidator(ValidatorYears(True, self.firstYear, self.lastYear, self.errorMessage))

        self._hoverStyleButton(self.makeDayCurveAmount)

    def OnMakeDayCurve(self, _):

        self._plotRawSmooth(int(self.firstYear.GetValue()), int(self.lastYear.GetValue()), DataColumn.amountRain,
                            True, True)
