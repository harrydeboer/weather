import wx
from panels.PagePanel import PagePanel
from validators.ValidatorFirstYearLastYear import ValidatorFirstYearLastYear
from models.DataColumn import DataColumn


class TemperaturePanel(PagePanel):

    def __init__(self, parent, knmi_data):

        super().__init__(parent, knmi_data)

        # The text_output shows the first day of summer or the temperature increase.
        self.text_output = wx.StaticText(self, -1, '')
        self.text_output.SetForegroundColour('#FFFFFF')

        # The make_day_curve and make_year_curve button click events are bound to callbacks and validators.
        self.make_day_curve = wx.Button(self, label='make day curve')
        self.make_day_curve.Bind(wx.EVT_BUTTON, self.on_make_day_curve_temp)
        self.make_day_curve.SetValidator(
            ValidatorFirstYearLastYear('dayCurve', self.first_year, self.last_year, self.error_message))
        self.make_year_curve = wx.Button(self, label="make year curve")
        self.make_year_curve.Bind(wx.EVT_BUTTON, self.on_make_year_curve_temp)
        self.make_year_curve.SetValidator(
            ValidatorFirstYearLastYear('yearCurve', self.first_year, self.last_year, self.error_message))

        self._hover_style_button(self.make_day_curve)
        self._hover_style_button(self.make_year_curve)

        sizer_v = wx.BoxSizer(wx.VERTICAL)
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h.Add(self.make_day_curve)
        sizer_h.Add(self.make_year_curve)
        sizer_v.Add(sizer_h)
        sizer_v.Add(self.text_output)

        self._add_to_page(sizer_v)

    def on_make_day_curve_temp(self, _):

        first_year = self.first_year.GetValue()
        last_year = self.last_year.GetValue()

        self._plot_raw_smooth(first_year, last_year, DataColumn.min_temp, True, True)
        curve = self._plot_raw_smooth(first_year, last_year, DataColumn.mean_temp, False, True)
        self._plot_raw_smooth(first_year, last_year, DataColumn.max_temp, False, True)

        self.text_output.SetLabel('First day of summer: ' + curve.get_first_date_summer().strftime("%d %B") + '.')

    def on_make_year_curve_temp(self, _):

        curve = self._plot_raw_smooth(self.first_year.GetValue(), self.last_year.GetValue(),
                                      DataColumn.mean_temp, True, False)

        self.text_output.SetLabel('Temperature increase: ' +
                                  str(int((curve.y_smooth[-1] - curve.y_smooth[0]) * 10) / 10) + "°.")
