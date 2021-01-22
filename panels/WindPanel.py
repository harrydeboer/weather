import wx
from panels.PagePanel import PagePanel
from services.DayYearArrayBuildService import DayYearArrayBuildService
from models.Curve import Curve
from models.DataColumn import DataColumn
from validators.ValidatorFirstYearLastYear import ValidatorFirstYearLastYear


class WindPanel(PagePanel):

    def __init__(self, parent, knmi_data):

        super().__init__(parent, knmi_data)

        self.info = wx.StaticText(self, -1, " The wind direction is an angle between 0 and 360 degrees. \n" +
                                  " 0 is east, 90 is north, 180 is west and 270 is south.")
        self.info.SetForegroundColour('#FFFFFF')

        # The makeDayCurveSpeed and makeDayCurveDirection button click events are bound to callbacks and validators.
        self.make_day_curve_speed = wx.Button(self, label='make day curve speed')
        self.make_day_curve_speed.Bind(wx.EVT_BUTTON, self.on_make_day_curve_speed)
        self.make_day_curve_speed.SetValidator(
            ValidatorFirstYearLastYear('dayCurve', self.first_year, self.last_year, self.error_message))
        self.make_day_curve_direction = wx.Button(self, label='make day curve direction')
        self.make_day_curve_direction.Bind(wx.EVT_BUTTON, self.on_make_day_curve_vector)
        self.make_day_curve_direction.SetValidator(
            ValidatorFirstYearLastYear('dayCurve', self.first_year, self.last_year, self.error_message))

        self._hover_style_button(self.make_day_curve_speed)
        self._hover_style_button(self.make_day_curve_direction)

        sizer_v = wx.BoxSizer(wx.VERTICAL)
        sizer_v.Add(self.info)
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h.Add(self.make_day_curve_speed)
        sizer_h.Add(self.make_day_curve_direction)
        sizer_v.Add(sizer_h)

        self._add_to_page(sizer_v)

    def on_make_day_curve_speed(self, _):

        self._plot_raw_smooth(self.first_year.GetValue(), self.last_year.GetValue(), DataColumn.wind_speed, True, True)

    def on_make_day_curve_vector(self, _):

        first_year = self.first_year.GetValue()
        last_year = self.last_year.GetValue()

        # The vector average speed and direction are retrieved as a 2 dimensional day year array.
        speed_2d = DayYearArrayBuildService.make_array(self.knmiData.array, first_year,
                                                       last_year, DataColumn.wind_speed_va)
        angle_2d = DayYearArrayBuildService.make_array(self.knmiData.array,
                                                       first_year, last_year, DataColumn.wind_direction)

        # The 2 dimensional angle and speed are averaged over the years.
        angle = Curve.mean_of_angle(speed_2d, angle_2d)

        curve = Curve(angle, True, first_year, last_year)

        self.plot_panel.plot(curve.x, curve.y, curve.y_smooth, True)
