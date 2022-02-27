"""
PlotWidget View is a view class for Matplotlib plot widget.

Author: Artem Shepelin
License: GPLv3
"""

import matplotlib as mpl
mpl.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class PlotWidget(FigureCanvas):
    def __init__(self, *args, **kwargs):
        self._dpi = 100
        if "dpi" in kwargs.keys():
            self._dpi = kwargs["dpi"]
        self._figure_x = 6
        if "figure_x" in kwargs.keys():
            self._figure_x = kwargs["figure_x"]
        self._figure_y = 4
        if "figure_y" in kwargs.keys():
            self._figure_y = kwargs["figure_y"]

        self.figure = Figure(figsize=(self._figure_x, self._figure_y),
                             dpi=self._dpi)
        self.ax = self.figure.add_subplot(1, 1, 1)

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        super().__init__(self.figure)

        self.setFixedSize(int(self._dpi * self._figure_x),
                          int(self._dpi * self._figure_y))

        self._axes_color = None
        self._axes_labels_color = None
        self._background_color = None
        self._data = None
        self._is_background_transparent = None
        self._is_show_intermediate_lines = None
        self._ticks_color = None
        self._title = None
        self._title_color = None
        self._x_axis_name = None
        self._x_max = None
        self._x_min = None
        self._y_axis_name = None
        self._y_max = None
        self._y_min = None


    def setAxesColor(self, axes_color):
        if self._axes_color != axes_color:
            self._axes_color = axes_color
            self._draw_axes_color()
            self.draw()


    def setAxesLabelsColor(self, axes_labels_color):
        if self._axes_labels_color != axes_labels_color:
            self._axes_labels_color = axes_labels_color
            self._draw_axes_labels_color()
            self.draw()


    def setBackgroundColor(self, background_color):
        if self._background_color != background_color:
            self._background_color = background_color
            self._draw_background()
            self.draw()


    def setData(self, data):
        self._data = data
        self._clear()
        self._draw_full()


    def setDpi(self, dpi):
        if self._dpi != dpi:
            self._dpi = dpi
            self._reset()


    def setFigureX(self, figure_x):
        if self._figure_x != figure_x:
            self._figure_x = figure_x
            self._reset()


    def setFigureY(self, figure_y):
        if self._figure_y != figure_y:
            self._figure_y = figure_y
            self._reset()


    def setIsBackgroundTransparent(self, is_background_transparent):
        if self._is_background_transparent != is_background_transparent:
            self._is_background_transparent = is_background_transparent
            self._draw_background()
            self.draw()


    def setIsShowIntermediateLines(self, is_show_intermediate_lines):
        if self._is_show_intermediate_lines != is_show_intermediate_lines:
            self._is_show_intermediate_lines = is_show_intermediate_lines
            self._clear()
            self._draw_full()


    def setTicksColor(self, ticks_color):
        if self._ticks_color != ticks_color:
            self._ticks_color = ticks_color
            self._draw_ticks_color()
            self.draw()


    def setTitle(self, title):
        if self._title != title:
            self._title = title
            try:
                self._draw_title()
                self.draw()
            except:
                pass


    def setTitleColor(self, title_color):
        if self._title_color != title_color:
            self._title_color = title_color
            self._draw_title_color()
            self.draw()


    def setXAxisName(self, x_axis_name):
        if self._x_axis_name != x_axis_name:
            self._x_axis_name = x_axis_name
            try:
                self._draw_x_axis_name()
                self.draw()
            except:
                pass


    def setXMax(self, x_max):
        if self._x_max != x_max:
            self._x_max = x_max
            self._draw_x_limits()
            self.draw()


    def setXMin(self, x_min):
        if self._x_min != x_min:
            self._x_min = x_min
            self._draw_x_limits()
            self.draw()


    def setYAxisName(self, y_axis_name):
        if self._y_axis_name != y_axis_name:
            self._y_axis_name = y_axis_name
            try:
                self._draw_y_axis_name()
                self.draw()
            except:
                pass


    def setYMax(self, y_max):
        if self._y_max != y_max:
            self._y_max = y_max
            self._draw_y_limits()
            self.draw()


    def setYMin(self, y_min):
        if self._y_min != y_min:
            self._y_min = y_min
            self._draw_y_limits()
            self.draw()


    def _clear(self):
        self.ax.clear()


    def _draw_axes_color(self):
        if self._axes_color:
            for axes in self.figure.axes:
                for spines in axes.spines.keys():
                    axes.spines[spines].set_color(self._axes_color)


    def _draw_axes_labels_color(self):
        if self._axes_labels_color:
            self.ax.xaxis.label.set_color(self._axes_labels_color)
            self.ax.yaxis.label.set_color(self._axes_labels_color)


    def _draw_background(self):
        self.figure.patch.set_facecolor(self._background_color)
        if self._is_background_transparent:
            self.ax.patch.set_alpha(0)
        else:
            self.figure.patch.set_alpha(1)
            self.ax.patch.set_facecolor(self._background_color)
            self.ax.patch.set_alpha(1)


    def _draw_full(self):
        self._draw_axes_color()
        self._draw_axes_labels_color()
        self._draw_background()
        self._draw_image()
        self._draw_ticks_color()
        self._draw_title()
        self._draw_title_color()
        self._draw_x_axis_name()
        self._draw_x_limits()
        self._draw_y_axis_name()
        self._draw_y_limits()
        self.draw()


    def _draw_image(self):
        # colors = ["#6c81ff", "#fffc6c", "#ff836c", "#88ff6c"]
        # colors = ["#00bcff", "#ffd300", "#ff2700", "#81ff00"]
        colors = ["#0EA5FF", "#FF3D00", "#00FF7D", "#FF8C00"]
        if not isinstance(self._data, type(None)):
            linewidth = 2
            if not self._is_show_intermediate_lines:
                self.ax.plot(self._data.index, self._data["F"],
                             color=colors[0], linewidth=linewidth)
            else:
                for i, key in enumerate(self._data.keys()):
                    self.ax.plot(self._data.index, self._data[key],
                                 color=colors[i % len(colors)],
                                 linewidth=linewidth)


    def _draw_ticks_color(self):
        if self._ticks_color:
            for axes in self.figure.axes:
                axes.tick_params(axis="x", colors=self._ticks_color)
                axes.tick_params(axis="y", colors=self._ticks_color)


    def _draw_title(self):
        self.ax.set_title(self._title, fontsize=14)


    def _draw_title_color(self):
        if self._title_color:
            self.ax.title.set_color(self._title_color)


    def _draw_x_axis_name(self):
        self.ax.set_xlabel(self._x_axis_name, fontsize=14)


    def _draw_x_limits(self):
        self.ax.set_xlim([self._x_min, self._x_max])


    def _draw_y_axis_name(self):
        self.ax.set_ylabel(self._y_axis_name, fontsize=14)


    def _draw_y_limits(self):
        self.ax.set_ylim([self._y_min, self._y_max])


    def _reset(self):
        self.figure = Figure(figsize=(self._figure_x, self._figure_y),
                             dpi=self._dpi)
        self.ax = self.figure.add_subplot(1, 1, 1)

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        self.setFixedSize(int(self._dpi * self._figure_x),
                          int(self._dpi * self._figure_y))
        self._draw_full()