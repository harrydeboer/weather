import wx
import wx.xrc as xrc
from panels.MainPanel import MainPanel
from panels.TemperaturePanel import TemperaturePanel
from panels.WindPanel import WindPanel
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

        # The notebook gets its pages which gives tabs on the top of the main panel.
        self.notebook = xrc.XRCCTRL(self.mainPanel, 'notebook')
        sizer.Add(self.notebook, 1, wx.EXPAND)
        pageTemperature = self.res.LoadPanel(self.notebook, 'temperature')
        TemperaturePanel(pageTemperature)
        pageWind = self.res.LoadPanel(self.notebook, 'wind')
        self.pageWind = WindPanel(pageWind)
        self.notebook.AddPage(pageTemperature, 'Temperature', True)
        self.notebook.AddPage(pageWind, 'Wind', True)
        self.notebook.ChangeSelection(0)

        self.mainFrame.Show(isShown)
        self.SetTopWindow(self.mainFrame)


if __name__ == '__main__':
    app = WeatherApp(True)
    app.MainLoop()
