import wx


class MainPanel(wx.Panel):

    def __init__(self, parent, width: int, height: int):

        super().__init__(parent, -1)

        self.width = width
        self.height = height
        self.SetBackgroundColour('#1C6CBC')
        self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
