import wx


# Validates the first year and last year when a curve is to be calculated.
class ValidatorYears(wx.Validator):

    def __init__(self, curveType: str, firstYear, lastYear, errorMessage):
        wx.Validator.__init__(self)
        self.Bind(wx.EVT_BUTTON, self.OnClick)
        self.firstYear = firstYear
        self.lastYear = lastYear
        self.curveType = curveType
        self.errorMessage = errorMessage
        self.firstYearInitial = int(firstYear.GetValue())
        self.lastYearInitial = int(lastYear.GetValue())

    def Clone(self):

        return ValidatorYears(self.curveType, self.firstYear, self.lastYear, self.errorMessage)

    def Validate(self, win):

        return True

    def TransferToWindow(self):

        return True

    def TransferFromWindow(self):

        return True

    def OnClick(self, event):

        firstYear = int(self.firstYear.GetValue())
        lastYear = int(self.lastYear.GetValue())

        if lastYear < firstYear:

            self.errorMessage.SetLabel('Last year cannot be smaller than first year.')

            return

        if firstYear < int(self.firstYearInitial) or lastYear > int(self.lastYearInitial):

            self.errorMessage.SetLabel('Years out of range ' +
                                       str(self.firstYearInitial) + '-' + str(self.lastYearInitial) + '.')

            return

        if self.curveType == 'yearCurve' and lastYear - firstYear < 5 - 1:

            self.errorMessage.SetLabel('Range should be 5 years at least when making a year curve.')

            return

        if self.curveType == 'rainPercentage' and firstYear < 1930:

            self.errorMessage.SetLabel('Range cannot be before 1930.')

            return

        self.errorMessage.SetLabel('')

        event.Skip()
