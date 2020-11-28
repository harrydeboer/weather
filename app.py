import wx
import wx.xrc as xrc
from panels.TemperaturePanel import TemperaturePanel
from panels.WindPanel import WindPanel
from models.KNMIData import KNMIData
import locale


class WeatherApp(wx.App):

    def __init__(self, isShown: bool):

        super().__init__()

        # The locale is en_GB to set the language on english.
        locale.setlocale(locale.LC_ALL, 'en_GB')

        sizer = wx.BoxSizer()
        self.res = xrc.XmlResource('layout/weather.xml')
        self.mainFrame = self.res.LoadFrame(None, 'mainFrame')
        self.mainPanel = xrc.XRCCTRL(self.mainFrame, 'mainPanel')
        self.mainPanel.SetSizer(sizer)
        self.mainPanel.Layout()
        knmiData = KNMIData()

        # The notebook gets its pages which gives tabs on the top of the main panel.
        self.notebook = xrc.XRCCTRL(self.mainPanel, 'notebook')
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.pageTemperature = TemperaturePanel(self.res.LoadPanel(self.notebook, 'temperature'), knmiData)
        self.pageWind = WindPanel(self.res.LoadPanel(self.notebook, 'wind'), knmiData)
        self.notebook.AddPage(self.pageTemperature.GetParent(), 'Temperature', True)
        self.notebook.AddPage(self.pageWind.GetParent(), 'Wind', True)
        self.notebook.ChangeSelection(0)

        self.mainFrame.Show(isShown)
        self.SetTopWindow(self.mainFrame)


if __name__ == '__main__':
    app = WeatherApp(True)
    app.MainLoop()
