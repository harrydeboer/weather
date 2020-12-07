import wx
from panels.TemperaturePanel import TemperaturePanel
from panels.WindPanel import WindPanel
from panels.SunshinePanel import SunshinePanel
from panels.RainPanel import RainPanel
from panels.TopPanel import TopPanel
from models.KNMIData import KNMIData
import locale


class WeatherApp(wx.App):

    def __init__(self, isShown: bool):

        super().__init__()

        # The locale is en_GB. This way the language is english.
        locale.setlocale(locale.LC_ALL, 'en_GB')

        self.mainFrame = wx.Frame(None, wx.ID_ANY, 'Weather', size=(550, 700))
        self.mainPanel = wx.Panel(self.mainFrame)
        self.mainPanel.SetBackgroundColour('#1C6CBC')
        self.mainPanel.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.topPanel = TopPanel(self.mainPanel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.topPanel, 0, wx.EXPAND)

        # Read the KNMI data once. The data is passed to the panels.
        knmiData = KNMIData()

        # The notebook is initialized and the pages are added.
        self.notebook = wx.Notebook(self.mainPanel)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.pageTemperature = TemperaturePanel(self.notebook, knmiData)
        self.pageWind = WindPanel(self.notebook, knmiData)
        self.pageSunshine = SunshinePanel(self.notebook, knmiData)
        self.pageRain = RainPanel(self.notebook, knmiData)
        self.notebook.AddPage(self.pageTemperature, 'Temperature', True)
        self.notebook.AddPage(self.pageWind, 'Wind', True)
        self.notebook.AddPage(self.pageSunshine, 'Sunshine', True)
        self.notebook.AddPage(self.pageRain, 'Rain', True)
        self.notebook.ChangeSelection(0)

        self.mainPanel.SetSizer(sizer)
        self.mainPanel.Layout()

        self.mainFrame.Show(isShown)
        self.SetTopWindow(self.mainFrame)


if __name__ == '__main__':
    app = WeatherApp(True)
    app.MainLoop()
