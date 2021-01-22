import wx
from panels.TemperaturePanel import TemperaturePanel
from panels.WindPanel import WindPanel
from panels.SunshinePanel import SunshinePanel
from panels.RainPanel import RainPanel
from panels.MainPanel import MainPanel
from panels.TopPanel import TopPanel
from models.KNMIData import KNMIData
import locale


class WeatherApp(wx.App):

    def __init__(self, is_shown: bool):

        super().__init__()

        # The locale is en_GB. This way the language is english.
        locale.setlocale(locale.LC_ALL, 'en_GB')

        width = 550
        height = 700

        self.mainFrame = wx.Frame(None, wx.ID_ANY, 'Weather', size=(width, height))
        self.mainPanel = MainPanel(self.mainFrame, width, height)
        self.topPanel = TopPanel(self.mainPanel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.topPanel, 0, wx.EXPAND)

        # Read the KNMI data once. The data is passed to the panels.
        knmi_data = KNMIData()

        # The notebook is initialized and the pages are added.
        self.notebook = wx.Notebook(self.mainPanel)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.page_temperature = TemperaturePanel(self.notebook, knmi_data)
        self.page_wind = WindPanel(self.notebook, knmi_data)
        self.page_sunshine = SunshinePanel(self.notebook, knmi_data)
        self.page_rain = RainPanel(self.notebook, knmi_data)
        self.notebook.AddPage(self.page_temperature, 'Temperature', True)
        self.notebook.AddPage(self.page_wind, 'Wind', True)
        self.notebook.AddPage(self.page_sunshine, 'Sunshine', True)
        self.notebook.AddPage(self.page_rain, 'Rain', True)
        self.notebook.ChangeSelection(0)

        self.mainPanel.SetSizer(sizer)
        self.mainPanel.Layout()

        self.mainFrame.Show(is_shown)
        self.SetTopWindow(self.mainFrame)


if __name__ == '__main__':
    app = WeatherApp(True)
    app.MainLoop()
