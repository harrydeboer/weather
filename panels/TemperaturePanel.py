import wx
import wx.xrc as xrc
from panels.PagePanel import PagePanel


class TemperaturePanel(PagePanel):

    def __init__(self, parent, knmiData):
        super().__init__(parent, knmiData)

        # The textOutput shows the first day of summer or the temperature increase.
        self.textOutput = xrc.XRCCTRL(parent, 'textOutput')

        # The makeDayCurve and makeYearCurve button click events are bound to callbacks.
        self.makeDayCurve = xrc.XRCCTRL(parent, "makeDayCurve")
        self.makeDayCurve.Bind(wx.EVT_BUTTON, self.OnMakeDayCurveTemp)
        self.makeYearCurve = xrc.XRCCTRL(parent, "makeYearCurve")
        self.makeYearCurve.Bind(wx.EVT_BUTTON, self.OnMakeYearCurveTemp)

        self._hoverStyleButton(self.makeDayCurve)
        self._hoverStyleButton(self.makeYearCurve)

    def OnMakeDayCurveTemp(self, _):

        firstYear, lastYear = self._validateYearRange('dayCurve', 'temperature')

        self._plotRawSmooth(firstYear, lastYear, 'minTemp', True, True)
        curve = self._plotRawSmooth(firstYear, lastYear, 'meanTemp', False, True)
        self._plotRawSmooth(firstYear, lastYear, 'maxTemp', False, True)

        self.textOutput.SetLabel('First day of summer: ' + curve.getFirstDateSummer().strftime("%d %B") + '.')

    def OnMakeYearCurveTemp(self, _):

        firstYear, lastYear = self._validateYearRange('yearCurve', 'temperature')

        curve = self._plotRawSmooth(firstYear, lastYear, 'meanTemp', True, False)

        self.textOutput.SetLabel('Temperature increase: ' +
                                 str(int((curve.ySmooth[-1] - curve.ySmooth[0]) * 10) / 10) + "°.")
