import wx
from wx.lib.intctrl import IntCtrl
from wx.core import StaticText


# Validates the first year and last year when a curve is to be calculated.
class ValidatorFirstYearLastYear(wx.Validator):

    def __init__(self, curve_type: str, first_year: IntCtrl, last_year: IntCtrl, error_message: StaticText):

        super().__init__()

        self.Bind(wx.EVT_BUTTON, self.on_click)
        self.first_year = first_year
        self.last_year = last_year
        self.curve_type = curve_type
        self.error_message = error_message
        self.first_year_initial = first_year.GetValue()
        self.last_year_initial = last_year.GetValue()

    def Clone(self):

        return ValidatorFirstYearLastYear(self.curve_type, self.first_year, self.last_year, self.error_message)

    def Validate(self, win):

        return True

    def TransferToWindow(self):

        return True

    def TransferFromWindow(self):

        return True

    def on_click(self, event):

        first_year = self.first_year.GetValue()
        last_year = self.last_year.GetValue()

        if last_year < first_year:

            self.error_message.SetLabel('Last year cannot be smaller than first year.')

            return

        if first_year < self.first_year_initial or last_year > self.last_year_initial:

            self.error_message.SetLabel('Years out of range ' +
                                        str(self.first_year_initial) + '-' + str(self.last_year_initial) + '.')

            return

        if self.curve_type == 'yearCurve' and last_year - first_year + 1 < 9:

            self.error_message.SetLabel('Range should be 9 years at least when making a year curve.')

            return

        if self.curve_type == 'rainPercentage' and first_year < 1930:

            self.error_message.SetLabel('Range cannot be before 1930.')

            return

        self.error_message.SetLabel('')

        event.Skip()
