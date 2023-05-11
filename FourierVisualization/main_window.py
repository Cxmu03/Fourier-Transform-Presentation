import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
import PyQt5.QtCore

from fourier_plotter import FourierPlotter
from canvas import Canvas

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')

import numpy as np

class FourierWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        self.app = QApplication(sys.argv)
        plt.ylim(-0.01, 0.01)
        plt.xlim(-0.01, 0.01)
        self.app.setStyleSheet("""
/* Set the background color of the entire application */
QWidget {
    background-color: #f2f2f2;
}

/* Set the color and font of the main window title */
QMainWindow::title {
    color: #333;
    font-family: Segoe UI;
    font-size: 16px;
    padding: 8px;
}

/* Set the background color and font of the main window menu bar */
QMenuBar {
    background-color: #fff;
    font-family: Segoe UI;
    font-size: 14px;
    padding: 8px;
}

/* Set the color of the main window menu bar items */
QMenuBar::item {
    color: #333;
}

/* Set the background color of the main window tool bar */
QToolBar {
    background-color: #fff;
    padding: 8px;
}

/* Set the color and font of the main window tool bar buttons */
QToolButton {
    color: #333;
    font-family: Segoe UI;
    font-size: 14px;
    padding: 8px;
}

/* Set the color and font of the main window status bar */
QStatusBar {
    color: #333;
    font-family: Segoe UI;
    font-size: 14px;
    padding: 8px;
}

/* Set the color and font of the main window central widget */
QWidget#centralWidget {
    color: #333;
    font-family: Segoe UI;
    font-size: 14px;
    padding: 16px;
}

/* Set the color and font of the main window buttons */
QPushButton {
    color: #fff;
    background-color: #007acc;
    font-family: Segoe UI;
    font-size: 14px;
    padding: 12px;
    border: none;
    border-radius: 4px;
    margin-right: 8px;
}

/* Set the color and font of the main window labels */
QLabel {
    color: #333;
    font-family: Segoe UI;
    font-size: 14px;
    padding: 8px;
    margin-bottom: 8px;
}

/* Set the style for the canvas */
Canvas {
    background-color: #fff;
    border: 1px solid #ccc;
}

/* Set the style for the QSlider */
QSlider {
    background-color: #fff;
    border: none;
}

/* Set the style for the QSlider groove */
QSlider::groove:horizontal {
    height: 4px;
    background-color: #ccc;
    margin: 0px;
}

/* Set the style for the QSlider handle */
QSlider::handle:horizontal {
    width: 10px;
    height: 10px;
    border-radius: 5px;
    background-color: #007acc;
    margin: -3px 0px;
}
        """)
        super(FourierWindow, self).__init__(*args, **kwargs)

        self.wrapping_frequency = 0

        self.plotter = FourierPlotter(0, 2)

        self.init_widgets()

        self.signal_plot.plot_data(self.plotter.signal())

        self.wrapped_signal_plot.plot_data(self.plotter.wrap_signal_around_point(0))
        
        self.show()

    def init_widgets(self):
        master_layout = QHBoxLayout(self)

        signal_layout = QVBoxLayout()

        graph_layout = QVBoxLayout()

        self.signal_plot = Canvas(self, width=5, height=4, dpi=100)

        signal_frequency_slider = QSlider(Qt.Horizontal)
        signal_frequency_slider.setRange(0, 300)
        signal_frequency_slider.setSingleStep(5)
        signal_frequency_slider.valueChanged.connect(self.on_signal_frequency_change)

        signal_progress_slider = QSlider(Qt.Horizontal)
        signal_progress_slider.setRange(0, 999)
        signal_progress_slider.setSingleStep(1)
        signal_progress_slider.valueChanged.connect(self.on_signal_progress_change)

        winding_frequency_slider = QSlider(Qt.Horizontal)
        winding_frequency_slider.setRange(0, 600)
        winding_frequency_slider.setSingleStep(1)
        winding_frequency_slider.valueChanged.connect(self.on_winding_frequency_change)

        self.wrapped_signal_plot = Canvas(self, width=5, height=4, dpi=100)
        self.mean_plot = Canvas(self, width=5, height=4, dpi=100)

        signal_layout.addWidget(signal_frequency_slider)
        signal_layout.addWidget(signal_progress_slider)
        signal_layout.addWidget(self.signal_plot)

        graph_layout.addWidget(winding_frequency_slider)
        graph_layout.addWidget(self.wrapped_signal_plot)
        graph_layout.addWidget(self.mean_plot)

        master_layout.addLayout(signal_layout)
        master_layout.addLayout(graph_layout)

        widget = QWidget()
        widget.setLayout(master_layout)

        self.setCentralWidget(widget)

    def on_signal_frequency_change(self, value):
        value = value / 100
        print(f"Signal Frequenz: {value}Hz")
        self.plotter.set_frequencies([(value, 1, 1, np.cos)])
        self.signal_plot.plot_data(self.plotter.signal())
        self.wrapped_signal_plot.plot_data(self.plotter.wrap_signal_around_point(self.wrapping_frequency))

        amplitude = self.plotter.calculate_amplitude()
        self.wrapped_signal_plot.axes.set_ylim([-amplitude, amplitude])
        self.wrapped_signal_plot.axes.set_xlim([-amplitude, amplitude])

    def on_signal_progress_change(self, value):
        self.plotter.set_progress(value)
        self.signal_plot.axes.clear()
        self.signal_plot.plot_data(self.plotter.signal())

        signal_x = self.plotter.signal()[0][value]
        signal_data = self.plotter.signal()[1][value]
        y_max = max(signal_data, 0)
        y_min = min(signal_data, 0)

        self.signal_plot.axes.vlines(self.plotter.progress, y_min, y_max, color="red")
        self.signal_plot.draw_idle()

        self.wrapped_signal_plot.axes.clear()
        self.wrapped_signal_plot.plot_data(self.plotter.wrapped_signal)
        self.wrapped_signal_plot.axes.arrow(0, 0, self.plotter.wrapped_signal[0][value], self.plotter.wrapped_signal[1][value], head_width=0.05, head_length=0.1, length_includes_head=True, color="red")
        self.wrapped_signal_plot.draw_idle()

    def on_winding_frequency_change(self, value):
        self.wrapping_frequency = value / 100
        print(f"Wicklungsfrequenz: {self.wrapping_frequency}Hz")
        x, y = self.plotter.wrap_signal_around_point(self.wrapping_frequency)
        mean = self.plotter.calculate_average_point()
        self.wrapped_signal_plot.plot_data((x, y))
        self.wrapped_signal_plot.axes.scatter(mean[0], mean[1], color="green")
        self.wrapped_signal_plot.axes.set_ylim([-self.plotter.amplitude, self.plotter.amplitude])
        self.wrapped_signal_plot.axes.set_xlim([-self.plotter.amplitude, self.plotter.amplitude])
        self.mean_plot.axes.clear()
        self.mean_plot.axes.plot(np.abs(np.array(self.plotter.average_point_signal)))
        self.mean_plot.draw_idle()

    def start(self):
        self.app.exec_()
