import wx


class MainPanel(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent, -1)

        self.SetBackgroundColour('#1C6CBC')
        self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
