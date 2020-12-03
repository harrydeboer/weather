import wx
import wx.xrc as xrc
from panels.PagePanel import PagePanel
from services.DateArrayBuildService import DateArrayBuildService
from models.Curve import Curve
from models.DataColumn import DataColumn
from validators.ValidatorYears import ValidatorYears


class WindPanel(PagePanel):

    def __init__(self, parent, knmiData):

        super().__init__(parent, knmiData)

        # The makeDayCurveSpeed and makeDayCurveDirection button click events are bound to callbacks.
        self.makeDayCurveSpeed = xrc.XRCCTRL(parent, "makeDayCurveSpeed")
        self.makeDayCurveSpeed.Bind(wx.EVT_BUTTON, self.OnMakeDayCurveSpeed)
        self.makeDayCurveSpeed.SetValidator(ValidatorYears('dayCurve', self.firstYear, self.lastYear, self.errorMessage))

        self.makeDayCurveDirection = xrc.XRCCTRL(parent, "makeDayCurveDirection")
        self.makeDayCurveDirection.Bind(wx.EVT_BUTTON, self.OnMakeDayCurveVector)
        self.makeDayCurveDirection.SetValidator(ValidatorYears('dayCurve', self.firstYear, self.lastYear, self.errorMessage))

        self._hoverStyleButton(self.makeDayCurveSpeed)
        self._hoverStyleButton(self.makeDayCurveDirection)

    def OnMakeDayCurveSpeed(self, _):

        self._plotRawSmooth(int(self.firstYear.GetValue()), int(self.lastYear.GetValue()), DataColumn.windSpeed, True, True)

    def OnMakeDayCurveVector(self, _):

        firstYear = int(self.firstYear.GetValue())
        lastYear = int(self.lastYear.GetValue())

        # The vector average speed and direction are retrieved as a 2 dimensional day year array.
        speed2D = DateArrayBuildService.makeArray(self.knmiData.array, firstYear, lastYear, DataColumn.windSpeedVA)
        angle2D = DateArrayBuildService.makeArray(self.knmiData.array, firstYear, lastYear, DataColumn.windDirection)

        # The 2 dimensional angle and speed are averaged over the years.
        angle = Curve.meanOfAngle(speed2D, angle2D)

        curve = Curve(angle, True, firstYear, lastYear)

        self.plotPanel.plot(curve.x, curve.y, curve.ySmooth, True)
