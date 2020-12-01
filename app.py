import wx
import wx.xrc as xrc
from panels.TemperaturePanel import TemperaturePanel
from panels.WindPanel import WindPanel
from models.KNMIData import KNMIData
import locale


class WeatherApp(wx.App):

    def __init__(self, isShown: bool):

        super().__init__()

        # The locale is en_GB. This way the language is english.
        locale.setlocale(locale.LC_ALL, 'en_GB')

        self.res = xrc.XmlResource('layout/weather.xml')
        self.mainFrame = self.res.LoadFrame(None, 'mainFrame')
        self.mainPanel = xrc.XRCCTRL(self.mainFrame, 'mainPanel')
        self.topPanel = xrc.XRCCTRL(self.mainFrame, 'topPanel')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.topPanel, 0, wx.EXPAND)

        # Read the KNMI data once. The data is passed to the panels.
        knmiData = KNMIData()

        # The notebook gets its pages which gives tabs on the top of the main panel.
        self.notebook = xrc.XRCCTRL(self.mainPanel, 'notebook')
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.pageTemperature = TemperaturePanel(self.res.LoadPanel(self.notebook, 'temperature'), knmiData)
        self.pageWind = WindPanel(self.res.LoadPanel(self.notebook, 'wind'), knmiData)
        self.notebook.AddPage(self.pageTemperature.GetParent(), 'Temperature', True)
        self.notebook.AddPage(self.pageWind.GetParent(), 'Wind', True)
        self.notebook.ChangeSelection(0)

        self.mainPanel.SetSizer(sizer)
        self.mainPanel.Layout()

        self.mainFrame.Show(isShown)
        self.SetTopWindow(self.mainFrame)


if __name__ == '__main__':
    app = WeatherApp(True)
    app.MainLoop()
