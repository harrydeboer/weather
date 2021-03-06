import wx
from wx.core import StaticText
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import datetime as dt
from models.Curve import Curve


class PlotPanel(wx.Panel):

    def __init__(self, parent):

        super().__init__(parent, -1)

        self.fig = Figure((5, 4), 75)
        self.canvas = FigureCanvas(self, -1, self.fig)
        self.axes = self.fig.add_subplot(111)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)

        self.SetSizer(sizer)
        self.Fit()

    def plot(self, x: np.ndarray, y: np.ndarray, y_smooth: np.ndarray, cla: bool):

        if cla:
            self.axes.cla()
        self.axes.plot(x, y)
        self.axes.plot(x, y_smooth)
        curves = self.axes.get_lines()

        # The legend of the day curves is added when the max is plotted. The mean legend is added to the year curve.
        if len(curves) == 6:
            self.axes.legend([curves[5], curves[3], curves[1]], ['max', 'mean', 'min'])
        else:
            self.axes.legend([curves[1]], ['mean'])

        self.canvas.draw()

    def on_plot_hover(self, event: MouseEvent, mouse_over: StaticText):

        for index, curve in enumerate(self.axes.get_lines()):

            # The curve is read when the mouse is precisely upon it.
            curve.set_pickradius(1)

            # The smooth plot is plotted after the raw plot. The raw is thus even and the smooth uneven.
            # The mouse over events are for the smooth plots only.
            if not index % 2 == 0:
                if curve.contains(event)[0]:

                    # The year plot has years (xdata) starting from 1906. The day plot has days (xdata) till 366.
                    # The year plot can thus be distinguished by the xdata being greater than 365.
                    if event.xdata > 366:
                        mouse_over.SetLabel("Mouse over curve: " + str(int(event.xdata)) +
                                            " " + str(int(event.ydata * 10) / 10))
                    else:
                        date = dt.datetime(2019, 1, 1) + dt.timedelta(int(event.xdata))
                        month_mean = Curve.get_month_mean(curve.get_ydata(), int(date.strftime("%m")), 2019)
                        mouse_over.SetLabel("Mouse over curve: " +
                                            date.strftime("%d %B") + " " + str(int(event.ydata * 10) / 10) + "\n"
                                            + "Month mean: " + str(int(month_mean * 10) / 10))
