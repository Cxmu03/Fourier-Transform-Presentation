import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets

from typing import List, Tuple

Left, Right = 1, 2
Top, Bottom = 4, 8
TopLeft = Top|Left
TopRight = Top|Right
BottomRight = Bottom|Right
BottomLeft = Bottom|Left

class Canvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(Canvas, self).__init__(fig)
        self.parent = parent

    def plot_data(self, data: Tuple[List, List]):
        self.axes.clear()
        self.axes.plot(data[0], data[1])
        self.draw_idle()

    def scatter_data(self, data: Tuple[List, List]):
        self.axes.clear()
        self.axes.scatter(data[0], data[1])
        self.draw_idle()
