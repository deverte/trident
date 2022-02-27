"""
Model is a module with a Model class that contains all application essential
data (only data). Extra `Property` class is used for ability to bind data with
each other and with widgets.
Development notes:
    To add a new data property:
    1) Define it inside `Model.__init__` function as Property.
    2) Add setter and getter of this property.

Author: Artem Shepelin
License: GPLv3
"""

import itertools
import os

import numpy as np
import pandas as pd

from trident.utils.property import Property


class Model:
    def __init__(self):
        self._lines_presets = {
            "Singlet" : {
                "multiplier": 1,
                "shifts": [0],
                "coefficients": [1]
            },
            "He II (2S3 > 2P3)": {
                "multiplier": 9.07,
                "shifts": [-30.5, 0, 2.8],
                "coefficients": [1 / 9, 3 / 9, 5 / 9]
            }
        }
        self._raw_dataframe = None

        self._axes_color = Property("#344291")
        self._axes_labels_color = Property("#4e63e3")
        self._background_color = Property("#0f1016")
        self._data = Property(None)
        self._dpi = Property(100)
        self._figure_x = Property(8)
        self._figure_y = Property(6)
        self._input_file = Property(None)
        self._is_show_intermediate_lines = Property(False)
        self._is_transparent_background = Property(True)
        self._lines_preset = Property("He II (2S3 > 2P3)")
        self._output_file = Property(None)
        self._ticks_color = Property("#4e63e3")
        self._title = Property("Title")
        self._title_color = Property("#4e63e3")
        self._x_axis_name = Property("X Axis")
        self._x_max = Property(1.0)
        self._x_min = Property(0.0)
        self._y_axis_name = Property("Y Axis")
        self._y_max = Property(1.0)
        self._y_min = Property(0.0)

        self._data.changed.connect(
            lambda data: self._x_max.setValue(data.index.max() + 5))
        self._data.changed.connect(
            lambda data: self._x_min.setValue(data.index.min() - 5))
        self._data.changed.connect(
            lambda data: self._y_max.setValue(data["F"].max() + 0.0005))
        self._data.changed.connect(
            lambda data: self._y_min.setValue(data["F"].min() - 0.0005))
        self._data.changed.connect(self._on_file_open)
        self._lines_preset.changed.connect(lambda : self._transform_data())


    @property
    def axes_color(self):
        return self._axes_color


    @axes_color.setter
    def axes_color(self, value):
        self._axes_color.setValue(value)


    @property
    def axes_labels_color(self):
        return self._axes_labels_color


    @axes_labels_color.setter
    def axes_color(self, value):
        self._axes_labels_color.setValue(value)


    @property
    def background_color(self):
        return self._background_color


    @background_color.setter
    def background_color(self, value):
        self._background_color.setValue(value)


    @property
    def data(self):
        return self._data


    @data.setter
    def data(self, file_path):
        if self.input_file.value != file_path:
            self.input_file = file_path
        if os.path.exists(file_path):
            try:
                self._raw_dataframe = pd.read_csv(
                    file_path, sep=" ", usecols=["VV", "FullAbs"])
                self._transform_data()
            except:
                raise Exception # Invalid File Format
                return
        else:
            raise FileNotFoundError


    def data_write(self, output_file, figure):
        if self.output_file.value != output_file:
            self.output_file = output_file

        path_head, path_tail = os.path.split(self.output_file.value)
        name, ext = os.path.splitext(path_tail)

        if ext in [".csv"]:
            self._data.value.to_csv(output_file)
        else:
            figure.savefig(self.output_file.value, dpi=self.dpi.value,
                           transparent=self.is_transparent_background.value)


    @property
    def dpi(self):
        return self._dpi


    @dpi.setter
    def dpi(self, value):
        self._dpi.setValue(value)


    @property
    def figure_x(self):
        return self._figure_x


    @figure_x.setter
    def figure_x(self, value):
        self._figure_x.setValue(value)


    @property
    def figure_y(self):
        return self._figure_y


    @figure_y.setter
    def figure_y(self, value):
        self._figure_y.setValue(value)


    @property
    def input_file(self):
        return self._input_file


    @input_file.setter
    def input_file(self, value):
        self._input_file.setValue(value)


    @property
    def is_show_intermediate_lines(self):
        return self._is_show_intermediate_lines


    @is_show_intermediate_lines.setter
    def is_show_intermediate_lines(self, value):
        self._is_show_intermediate_lines.setValue(value)


    @property
    def is_transparent_background(self):
        return self._is_transparent_background


    @is_transparent_background.setter
    def is_transparent_background(self, value):
        self._is_transparent_background.setValue(value)


    @property
    def lines_presets(self):
        return self._lines_presets


    @property
    def lines_preset(self):
        return self._lines_preset


    @lines_preset.setter
    def lines_preset(self, value):
        self._lines_preset.setValue(value)


    @property
    def output_file(self):
        return self._output_file


    @output_file.setter
    def output_file(self, value):
        self._output_file.setValue(value)


    @property
    def ticks_color(self):
        return self._ticks_color


    @ticks_color.setter
    def ticks_color(self, value):
        self._ticks_color.setValue(value)


    @property
    def title(self):
        return self._title


    @title.setter
    def title(self, value):
        self._title.setValue(value)


    @property
    def title_color(self):
        return self._title_color


    @title_color.setter
    def title_color(self, value):
        self._title_color.setValue(value)


    @property
    def x_axis_name(self):
        return self._x_axis_name


    @x_axis_name.setter
    def x_axis_name(self, value):
        self._x_axis_name.setValue(value)


    @property
    def x_max(self):
        return self._x_max


    @x_max.setter
    def x_max(self, value):
        self._x_max.setValue(value)


    @property
    def x_min(self):
        return self._x_min


    @x_min.setter
    def x_min(self, value):
        self._x_min.setValue(value)


    @property
    def y_axis_name(self):
        return self._y_axis_name


    @y_axis_name.setter
    def y_axis_name(self, value):
        self._y_axis_name.setValue(value)


    @property
    def y_max(self):
        return self._y_max


    @y_max.setter
    def y_max(self, value):
        self._y_max.setValue(value)


    @property
    def y_min(self):
        return self._y_min


    @y_min.setter
    def y_min(self, value):
        self._y_min.setValue(value)


    def _on_file_open(self):
        path_head, path_tail = os.path.split(self.input_file.value)
        name, ext = os.path.splitext(path_tail)
        self.output_file = os.path.join(path_head, name + ".png")


    def _transform_data(self):
        if not isinstance(self._raw_dataframe, type(None)):
            preset = self._lines_presets[self._lines_preset.value]
            multiplier = preset["multiplier"]
            shifts = preset["shifts"]
            coefficients = preset["coefficients"]

            vv = self._raw_dataframe["VV"]
            shifted_f = (self._raw_dataframe["FullAbs"] -
                         np.min(self._raw_dataframe["FullAbs"]))

            va = vv * multiplier

            vi = [va + shift for shift in shifts]
            fi = [shifted_f * coeff for coeff in coefficients]

            vs = np.sort(list(itertools.accumulate(vi, func=np.append))[-1])

            get_xs = lambda x_all, x_peak: x_all[(np.min(x_peak) <= x_all) &
                                                 (x_all <= np.max(x_peak))]
            interp_peak = lambda x_all, x_peak, y_peak: (
                np.interp(get_xs(x_all, x_peak), x_peak, y_peak))

            interp_dfs = [pd.DataFrame(interp_peak(vs, v, f),
                                       index=get_xs(vs, v), columns=["F"])
                          for (v, f) in zip(vi, fi)]

            df_res = list(
                itertools.accumulate(
                    interp_dfs,
                    lambda prv, nxt: prv.add(nxt, fill_value=0.0)))[-1]
            if len(coefficients) > 1:
                for i, coefficient in enumerate(coefficients):
                    df_res[f"{coefficient}"] = interp_dfs[i]

            self._data.setValue(df_res)