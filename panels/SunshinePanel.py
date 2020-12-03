import wx
import wx.xrc as xrc
from panels.PagePanel import PagePanel
from models.DataColumn import DataColumn
from validators.ValidatorYears import ValidatorYears


class SunshinePanel(PagePanel):

    def __init__(self, parent, knmiData):

        super().__init__(parent, knmiData)

        # The makeDayCurveSpeed and makeDayCurveDirection button click events are bound to callbacks.
        self.makeDayCurve = xrc.XRCCTRL(parent, "makeDayCurve")
        self.makeDayCurve.Bind(wx.EVT_BUTTON, self.OnMakeDayCurve)
        self.makeDayCurve.SetValidator(ValidatorYears('dayCurve', self.firstYear, self.lastYear, self.errorMessage))

        self._hoverStyleButton(self.makeDayCurve)

    def OnMakeDayCurve(self, _):

        self._plotRawSmooth(int(self.firstYear.GetValue()), int(self.lastYear.GetValue()), DataColumn.percSunshine,
                            True, True)
