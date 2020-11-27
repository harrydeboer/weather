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

        # When the mouse hovers over the makeDayCurveSpeed and makeDayCurveDirection buttons the button text
        # turns black and when the mouse leaves the text is white again.
        self.makeDayCurveSpeed.Bind(wx.EVT_ENTER_WINDOW,
                                    lambda event: self.makeDayCurveSpeed.SetForegroundColour('#000000'))
        self.makeDayCurveSpeed.Bind(wx.EVT_LEAVE_WINDOW,
                                    lambda event: self.makeDayCurveSpeed.SetForegroundColour('#FFFFFF'))
        self.makeDayCurveDirection.Bind(wx.EVT_ENTER_WINDOW,
                                        lambda event: self.makeDayCurveDirection.SetForegroundColour('#000000'))
        self.makeDayCurveDirection.Bind(wx.EVT_LEAVE_WINDOW,
                                        lambda event: self.makeDayCurveDirection.SetForegroundColour('#FFFFFF'))

    def OnMakeDayCurveWind(self, _):

        firstYear, lastYear = self._validateYearRange('dayCurve', 'wind')
        self._plotRawSmooth(firstYear, lastYear, 'windSpeed', True, True)

    def OnMakeDayCurveVector(self, _):

        firstYear, lastYear = self._validateYearRange('dayCurve', 'wind')
        speed2D = DateArrayBuildService.makeArray(self.knmiData.array, firstYear, lastYear, 'windSpeedVA')
        angle2D = DateArrayBuildService.makeArray(self.knmiData.array, firstYear, lastYear, 'windDirection')

        angle = Curve.meanOfAngle(speed2D, angle2D)

        curve = Curve(angle, True, firstYear, lastYear)

        self.plotPanel.plot(curve.x, curve.y, curve.ySmooth, True)
