import wx


class TopPanel(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent, -1)

        width = 550

        title = wx.StaticText(self, -1, 'Check out this weather app!', style=wx.ALIGN_CENTER, size=(width, 50))
        title.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour('#FFFFFF')

        text = wx.StaticText(self, -1,
                             """This app analyses the weather of De Bilt. The weather data can be averaged 
            by years or days resulting in a day curve or a year curve. The data can be 
            analysed starting at some year and ending in another. The raw curves are 
            smoothed with a filter. The mouse over is enabled for the smooth curves only 
            and shows the date and value at that point of the curve. The first day of 
            summer is calculated from defining summer as the warmest three months of 
            the year. The temperature increase over the years is shown with the year 
            curve. Curves can be also be made for wind, sunshine and rain.""",
                             style=wx.ALIGN_CENTER)

        text.SetForegroundColour('#FFFFFF')

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(title)
        sizer.Add(text)

        self.SetSizer(sizer)
        self.Layout()
