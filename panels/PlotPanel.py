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

        wx.Panel.__init__(self, parent, -1)

        self.fig = Figure((5, 4), 75)
        self.canvas = FigureCanvas(self, -1, self.fig)
        self.axes = self.fig.add_subplot(111)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)

        self.SetSizer(sizer)
        self.Fit()

    def plot(self, x: np.ndarray, y: np.ndarray, ySmooth: np.ndarray, cla: bool):

        if cla:
            self.axes.cla()
        self.axes.plot(x, y)
        self.axes.plot(x, ySmooth)
        curves = self.axes.get_lines()

        # The legend of the day curves is added when the max is plotted. The mean legend is added to the year curve.
        if len(curves) == 6:
            self.axes.legend([curves[5], curves[3], curves[1]], ['max', 'mean', 'min'])
        else:
            self.axes.legend([curves[1]], ['mean'])

        self.canvas.draw()

    def onPlotHover(self, event: MouseEvent, mouseOver: StaticText):

        for index, curve in enumerate(self.axes.get_lines()):

            # The curve is read only when the mouse is precisely upon it.
            curve.set_pickradius(1)

            # The smooth plot is plotted after the raw plot. The raw is thus even and the smooth uneven.
            if not index % 2 == 0:
                if curve.contains(event)[0]:

                    # The year plot has years (xdata) starting from 1901. The day plot has days (xdata) till 366.
                    # The year plot can thus be distinguished by the xdata being greater than 365.
                    if event.xdata > 366:
                        mouseOver.SetLabel("Mouse over curve: " + str(int(event.xdata)) +
                                           " " + str(int(event.ydata * 10) / 10))
                    else:
                        date = dt.datetime(2019, 1, 1) + dt.timedelta(int(event.xdata))
                        monthMean = Curve.getMonthMean(curve.get_ydata(), int(date.strftime("%m")), 2019)
                        mouseOver.SetLabel("Mouse over curve: " +
                                           date.strftime("%d %B") + " " + str(int(event.ydata * 10) / 10) + "\n"
                                           + "Month mean: " + str(int(monthMean * 10) / 10))
