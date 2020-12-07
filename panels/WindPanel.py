import wx
from panels.PagePanel import PagePanel
from services.DayYearArrayBuildService import DayYearArrayBuildService
from models.Curve import Curve
from models.DataColumn import DataColumn
from validators.ValidatorYears import ValidatorYears


class WindPanel(PagePanel):

    def __init__(self, parent, knmiData):
        super().__init__(parent, knmiData)

        self.info = wx.StaticText(self, -1, """The wind direction is an angle between 0 and 360 degrees.
                                  0 is east, 90 is north, 180 is west and 270 is south.""")
        self.info.SetForegroundColour('#FFFFFF')

        # The makeDayCurveSpeed and makeDayCurveDirection button click events are bound to callbacks.
        self.makeDayCurveSpeed = wx.Button(self, label='make day curve speed')
        self.makeDayCurveSpeed.Bind(wx.EVT_BUTTON, self.OnMakeDayCurveSpeed)
        self.makeDayCurveSpeed.SetValidator(ValidatorYears('dayCurve',
                                                           self.firstYear, self.lastYear, self.errorMessage))

        self.makeDayCurveDirection = wx.Button(self, label='make day curve direction')
        self.makeDayCurveDirection.Bind(wx.EVT_BUTTON, self.OnMakeDayCurveVector)
        self.makeDayCurveDirection.SetValidator(ValidatorYears('dayCurve',
                                                               self.firstYear, self.lastYear, self.errorMessage))

        self._hoverStyleButton(self.makeDayCurveSpeed)
        self._hoverStyleButton(self.makeDayCurveDirection)

        sizerV = wx.BoxSizer(wx.VERTICAL)
        sizerV.Add(self.info)
        sizerH = wx.BoxSizer(wx.HORIZONTAL)
        sizerH.Add(self.makeDayCurveSpeed)
        sizerH.Add(self.makeDayCurveDirection)
        sizerV.Add(sizerH)

        self._addToPage(sizerV)

    def OnMakeDayCurveSpeed(self, _):
        self._plotRawSmooth(int(self.firstYear.GetValue()), int(self.lastYear.GetValue()),
                            DataColumn.windSpeed, True, True)

    def OnMakeDayCurveVector(self, _):
        firstYear = int(self.firstYear.GetValue())
        lastYear = int(self.lastYear.GetValue())

        # The vector average speed and direction are retrieved as a 2 dimensional day year array.
        speed2D = DayYearArrayBuildService.makeArray(self.knmiData.array, firstYear, lastYear, DataColumn.windSpeedVA)
        angle2D = DayYearArrayBuildService.makeArray(self.knmiData.array,
                                                     firstYear, lastYear, DataColumn.windDirection)

        # The 2 dimensional angle and speed are averaged over the years.
        angle = Curve.meanOfAngle(speed2D, angle2D)

        curve = Curve(angle, True, firstYear, lastYear)

        self.plotPanel.plot(curve.x, curve.y, curve.ySmooth, True)
