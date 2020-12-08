import wx
from wx.lib.intctrl import IntCtrl
from wx.core import StaticText


# Validates the first year and last year when a curve is to be calculated.
class ValidatorFirstYearLastYear(wx.Validator):

    def __init__(self, curveType: str, firstYear: IntCtrl, lastYear: IntCtrl, errorMessage: StaticText):

        super().__init__()

        self.Bind(wx.EVT_BUTTON, self.OnClick)
        self.firstYear = firstYear
        self.lastYear = lastYear
        self.curveType = curveType
        self.errorMessage = errorMessage
        self.firstYearInitial = firstYear.GetValue()
        self.lastYearInitial = lastYear.GetValue()

    def Clone(self):

        return ValidatorFirstYearLastYear(self.curveType, self.firstYear, self.lastYear, self.errorMessage)

    def Validate(self, win):

        return True

    def TransferToWindow(self):

        return True

    def TransferFromWindow(self):

        return True

    def OnClick(self, event):

        firstYear = self.firstYear.GetValue()
        lastYear = self.lastYear.GetValue()

        if lastYear < firstYear:

            self.errorMessage.SetLabel('Last year cannot be smaller than first year.')

            return

        if firstYear < self.firstYearInitial or lastYear > self.lastYearInitial:

            self.errorMessage.SetLabel('Years out of range ' +
                                       str(self.firstYearInitial) + '-' + str(self.lastYearInitial) + '.')

            return

        if self.curveType == 'yearCurve' and lastYear - firstYear + 1 < 9:

            self.errorMessage.SetLabel('Range should be 9 years at least when making a year curve.')

            return

        if self.curveType == 'rainPercentage' and firstYear < 1930:

            self.errorMessage.SetLabel('Range cannot be before 1930.')

            return

        self.errorMessage.SetLabel('')

        event.Skip()
