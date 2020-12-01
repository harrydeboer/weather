import wx
import wx.xrc as xrc
from panels.PagePanel import PagePanel
from services.DateArrayBuildService import DateArrayBuildService
from models.Curve import Curve


class WindPanel(PagePanel):

    def __init__(self, parent, knmiData):

        super().__init__(parent, knmiData)

        # The makeDayCurveSpeed and makeDayCurveDirection button click events are bound to callbacks.
        self.makeDayCurveSpeed = xrc.XRCCTRL(parent, "makeDayCurveSpeed")
        self.makeDayCurveSpeed.Bind(wx.EVT_BUTTON, self.OnMakeDayCurveWind)
        self.makeDayCurveDirection = xrc.XRCCTRL(parent, "makeDayCurveDirection")
        self.makeDayCurveDirection.Bind(wx.EVT_BUTTON, self.OnMakeDayCurveVector)

        self._hoverStyleButton(self.makeDayCurveSpeed)
        self._hoverStyleButton(self.makeDayCurveDirection)

    def OnMakeDayCurveWind(self, _):

        firstYear, lastYear = self._validateYearRange('dayCurve')

        self._plotRawSmooth(firstYear, lastYear, 'windSpeed', True, True)

    def OnMakeDayCurveVector(self, _):

        firstYear, lastYear = self._validateYearRange('dayCurve')

        # The vector average speed and direction are retrieved as a 2 dimensional day year array.
        speed2D = DateArrayBuildService.makeArray(self.knmiData.array, firstYear, lastYear, 'windSpeedVA')
        angle2D = DateArrayBuildService.makeArray(self.knmiData.array, firstYear, lastYear, 'windDirection')

        # The 2 dimensional angle and speed are averaged over the years.
        angle = Curve.meanOfAngle(speed2D, angle2D)

        curve = Curve(angle, True, firstYear, lastYear)

        self.plotPanel.plot(curve.x, curve.y, curve.ySmooth, True)
