import wx
from panels.PagePanel import PagePanel
from models.DataColumn import DataColumn
from validators.ValidatorFirstYearLastYear import ValidatorFirstYearLastYear


class RainPanel(PagePanel):

    def __init__(self, parent, knmi_data):

        super().__init__(parent, knmi_data)

        # The make_day_curve_amount and make_day_curve_percentage button click events
        # are bound to callbacks and validators.
        self.make_day_curve_amount = wx.Button(self, label='make day curve amount')
        self.make_day_curve_amount.Bind(wx.EVT_BUTTON, self.on_make_day_curve)
        self.make_day_curve_amount.SetValidator(
            ValidatorFirstYearLastYear('dayCurve', self.first_year, self.last_year, self.error_message))
        self.make_day_curve_percentage = wx.Button(self, label='make day curve percentage')
        self.make_day_curve_percentage.Bind(wx.EVT_BUTTON, self.on_make_day_curve_percentage)
        self.make_day_curve_percentage.SetValidator(
            ValidatorFirstYearLastYear('rainPercentage', self.first_year, self.last_year, self.error_message))

        self._hover_style_button(self.make_day_curve_amount)
        self._hover_style_button(self.make_day_curve_percentage)

        sizer_v = wx.BoxSizer(wx.VERTICAL)
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h.Add(self.make_day_curve_amount)
        sizer_h.Add(self.make_day_curve_percentage)
        sizer_v.Add(sizer_h)

        self._add_to_page(sizer_v)

    def on_make_day_curve(self, _):

        self._plot_raw_smooth(self.first_year.GetValue(), self.last_year.GetValue(), DataColumn.amount_rain, True, True)

    def on_make_day_curve_percentage(self, _):

        self._plot_raw_smooth(self.first_year.GetValue(), self.last_year.GetValue(), DataColumn.perc_rain, True, True)
