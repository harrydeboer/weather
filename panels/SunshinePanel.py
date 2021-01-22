import wx
from panels.PagePanel import PagePanel
from models.DataColumn import DataColumn
from validators.ValidatorFirstYearLastYear import ValidatorFirstYearLastYear


class SunshinePanel(PagePanel):

    def __init__(self, parent, knmi_data):

        super().__init__(parent, knmi_data)

        # The make_day_curve button click event is bound to a callback and a validator.
        self.make_day_curve_percentage = wx.Button(self, label='make day curve percentage')
        self.make_day_curve_percentage.Bind(wx.EVT_BUTTON, self.on_make_day_curve)
        self.make_day_curve_percentage.SetValidator(
            ValidatorFirstYearLastYear('dayCurve', self.first_year, self.last_year, self.error_message))

        self._hover_style_button(self.make_day_curve_percentage)

        sizer_v = wx.BoxSizer(wx.VERTICAL)
        sizer_v.Add(self.make_day_curve_percentage)

        self._add_to_page(sizer_v)

    def on_make_day_curve(self, _):

        self._plot_raw_smooth(self.first_year.GetValue(), self.last_year.GetValue(),
                              DataColumn.perc_sunshine, True, True)
