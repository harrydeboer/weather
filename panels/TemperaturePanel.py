import wx
import wx.xrc as xrc
from panels.PagePanel import PagePanel
from validators.ValidatorYears import ValidatorYears


class TemperaturePanel(PagePanel):

    def __init__(self, parent, knmiData):
        super().__init__(parent, knmiData)

        # The textOutput shows the first day of summer or the temperature increase.
        self.textOutput = xrc.XRCCTRL(parent, 'textOutput')

        # The makeDayCurve and makeYearCurve button click events are bound to callbacks.
        self.makeDayCurve = xrc.XRCCTRL(parent, "makeDayCurve")
        self.makeDayCurve.Bind(wx.EVT_BUTTON, self.OnMakeDayCurveTemp)
        self.makeDayCurve.SetValidator(ValidatorYears(True, self.firstYear, self.lastYear, self.errorMessage))

        self.makeYearCurve = xrc.XRCCTRL(parent, "makeYearCurve")
        self.makeYearCurve.Bind(wx.EVT_BUTTON, self.OnMakeYearCurveTemp)
        self.makeYearCurve.SetValidator(ValidatorYears(False, self.firstYear, self.lastYear, self.errorMessage))

        self._hoverStyleButton(self.makeDayCurve)
        self._hoverStyleButton(self.makeYearCurve)

    def OnMakeDayCurveTemp(self, _):

        firstYear = int(self.firstYear.GetValue())
        lastYear = int(self.lastYear.GetValue())

        self._plotRawSmooth(firstYear, lastYear, 'minTemp', True, True)
        curve = self._plotRawSmooth(firstYear, lastYear, 'meanTemp', False, True)
        self._plotRawSmooth(firstYear, lastYear, 'maxTemp', False, True)

        self.textOutput.SetLabel('First day of summer: ' + curve.getFirstDateSummer().strftime("%d %B") + '.')

    def OnMakeYearCurveTemp(self, _):

        curve = self._plotRawSmooth(int(self.firstYear.GetValue()), int(self.lastYear.GetValue()),
                                    'meanTemp', True, False)

        self.textOutput.SetLabel('Temperature increase: ' +
                                 str(int((curve.ySmooth[-1] - curve.ySmooth[0]) * 10) / 10) + "°.")
