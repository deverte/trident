"""
Presenter is a module that connects model and view. It contains main application
presenter, that initializes view's initial values and binds data between model
and view. It also contains some helper functions that helps to transform data.
Development notes:
    1) You can initialize initial widget's value at
    `MainWindowPresenter._set_view_initial_values`.
    2) You can bind widget's value changes to a model using signals/slots at
    `MainWindowPresenter._bind_view_to_model` function.
    3) You can bind model's value changes to a view using signals/slots at
    `MainWindowPresenter._bind_model_to_view` function.
    4) You can add actions (for menus and etc.).
    5) You can add additional validators and helper data transformer methods.

Author: Artem Shepelin
License: GPLv3
"""

import os

from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QErrorMessage
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QMessageBox
AcceptSave = QFileDialog.AcceptMode.AcceptSave

from trident.ui.lines_table.model import LinesTableModel
from trident.__init__ import __version__


class MainWindowPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self._set_view_initial_values()
        self._bind_model_to_view()
        self._bind_view_to_model()


    def _action_about(self):
        QMessageBox.about(self.view, "About Trident",
            "Trident is a program for transforming singlet absorption lines to "
            "triplets and visualizing them.\n"
            "\n"
            f"Version: {__version__}\n"
            "Author: Artem Shepelin\n"
            "License: GPLv3\n"
            "Repository: https://github.com/deverte/trident")


    def _action_open_as(self):
        try:
            file_name = QFileDialog.getOpenFileName(
                self.view, "Open File", "",
                "Data Files (*.dat);;All Files (*.*)")[0]
            if file_name:
                self.model.data = file_name
        except FileNotFoundError:
            QErrorMessage(self.view).showMessage(
                f"File {self.model.input_file.value} does not exist.")
        except Exception:
            QErrorMessage(self.view).showMessage(
                f"File {self.model.input_file.value} has an incompatible format.")


    def _action_open(self):
        try:
            self.model.data = self.model.input_file.value
        except FileNotFoundError:
            QErrorMessage(self.view).showMessage(
                f"File {self.model.input_file.value} does not exist.")
        except Exception:
            QErrorMessage(self.view).showMessage(
                f"File {self.model.input_file.value} has an incompatible format.")


    def _action_save_as(self):
        if isinstance(self.model.data.value, type(None)):
            QErrorMessage(self.view).showMessage("Nothing to save.")
            return
        ftypes = [f"{val} (*.{key})" for key, val
                  in [*self.view.plotPlotWidget.get_supported_filetypes().items(),
                      ["csv", "Comma Separated Values"]]]
        save_file_dialog = QFileDialog(self.view)
        file_path = os.path.split(self.model.input_file.value)[0]
        if os.path.exists(file_path):
            save_file_dialog.setDirectory(file_path)
        save_file_dialog.setNameFilter(";;".join(ftypes))
        save_file_dialog.selectNameFilter(ftypes[5]) # png
        save_file_dialog.setAcceptMode(AcceptSave)
        if save_file_dialog.exec():
            file_name = save_file_dialog.selectedFiles()[0]
            name_filter = save_file_dialog.selectedNameFilter()
            file_ext = name_filter[name_filter.index("*") + 1:-1]

            path_head, path_tail = os.path.split(file_name)
            name, ext = os.path.splitext(path_tail)

            if ext != file_ext:
                file_name = f"{file_name}{file_ext}"
            if file_name:
                try:
                    self.model.data_write(file_name,
                                          self.view.plotPlotWidget.figure)
                except:
                    QErrorMessage(self.view).showMessage(
                        f"Can't save file {file_name}.")


    def _action_save(self):
        if isinstance(self.model.data.value, type(None)):
            QErrorMessage(self.view).showMessage("Nothing to save.")
            return
        file_path = os.path.split(self.model.input_file.value)[0]
        if not os.path.exists(file_path):
            QErrorMessage(self.view).showMessage(
                f"Path {file_path} does not exist.")
            return
        if not self.model.output_file.value:
            QErrorMessage(self.view).showMessage(
                f"Please, configure output file name.")
            return
        try:
            self.model.data_write(self.model.output_file.value,
                                  self.view.plotPlotWidget.figure)
        except:
            QErrorMessage(self.view).showMessage(
                f"Can't save file {self.model.output_file.value}.")


    def _bind_model_to_view(self):
        self.model.axes_color.changed.connect(self.view.plotPlotWidget.setAxesColor)
        self.model.axes_labels_color.changed.connect(self.view.plotPlotWidget.setAxesLabelsColor)
        self.model.background_color.changed.connect(self.view.plotPlotWidget.setBackgroundColor)
        self.model.data.changed.connect(self.view.plotPlotWidget.setData)
        self.model.dpi.changed.connect(self.view.plotPlotWidget.setDpi)
        self.model.figure_x.changed.connect(self.view.plotPlotWidget.setFigureX)
        self.model.figure_y.changed.connect(self.view.plotPlotWidget.setFigureY)
        self.model.input_file.changed.connect(self.view.inputFileFileLineEdit.setText)
        self.model.is_show_intermediate_lines.changed.connect(self.view.plotPlotWidget.setIsShowIntermediateLines)
        self.model.is_transparent_background.changed.connect(self.view.plotPlotWidget.setIsBackgroundTransparent)
        self.model.output_file.changed.connect(self.view.outputFileLineEdit.setText)
        self.model.ticks_color.changed.connect(self.view.plotPlotWidget.setTicksColor)
        self.model.title.changed.connect(self.view.plotPlotWidget.setTitle)
        self.model.title_color.changed.connect(self.view.plotPlotWidget.setTitleColor)
        self.model.x_axis_name.changed.connect(self.view.plotPlotWidget.setXAxisName)
        self.model.x_max.changed.connect(self.view.plotPlotWidget.setXMax)
        self.model.x_max.changed.connect(self.view.xMaxDoubleSpinBox.setValue)
        self.model.x_min.changed.connect(self.view.plotPlotWidget.setXMin)
        self.model.x_min.changed.connect(self.view.xMinDoubleSpinBox.setValue)
        self.model.y_axis_name.changed.connect(self.view.plotPlotWidget.setYAxisName)
        self.model.y_max.changed.connect(self.view.plotPlotWidget.setYMax)
        self.model.y_max.changed.connect(self.view.yMaxDoubleSpinBox.setValue)
        self.model.y_min.changed.connect(self.view.plotPlotWidget.setYMin)
        self.model.y_min.changed.connect(self.view.yMinDoubleSpinBox.setValue)
        self.model.lines_preset.changed.connect(lambda : self.view.linesConfigurationTableView.setModel(LinesTableModel(self.model.lines_presets[self.model.lines_preset.value])))


    def _bind_view_to_model(self):
        self.view.actionAbout.triggered.connect(self._action_about)
        self.view.actionOpen.triggered.connect(self._action_open_as)
        self.view.actionQuit.triggered.connect(lambda : sys.exit())
        self.view.actionSave.triggered.connect(self._action_save)
        self.view.actionSave_As.triggered.connect(self._action_save_as)
        self.view.axesColorColorButton.colorChanged.connect(self.model.axes_color.setValue)
        self.view.axesLabelsColorColorButton.colorChanged.connect(self.model.axes_labels_color.setValue)
        self.view.backgroundColorColorButton.colorChanged.connect(self.model.background_color.setValue)
        self.view.dpiSpinBox.valueChanged.connect(self.model.dpi.setValue)
        self.view.figureXDoubleSpinBox.valueChanged.connect(self.model.figure_x.setValue)
        self.view.figureYDoubleSpinBox.valueChanged.connect(self.model.figure_y.setValue)
        self.view.inputFileFileLineEdit.dropped.connect(self.model.input_file.setValue)
        self.view.inputFileFileLineEdit.editingFinished.connect(lambda : self.model.input_file.setValue(self.view.inputFileFileLineEdit.text()))
        self.view.isShowIntermediateLinesCheckBox.stateChanged.connect(self.model.is_show_intermediate_lines.setValue)
        self.view.isTransparentBackgroundCheckBox.stateChanged.connect(self.model.is_transparent_background.setValue)
        self.view.linesPresetComboBox.currentTextChanged.connect(self.model.lines_preset.setValue)
        self.view.openAsPushButton.pressed.connect(self._action_open_as)
        self.view.openPushButton.pressed.connect(self._action_open)
        self.view.outputFileLineEdit.editingFinished.connect(lambda : self.model.output_file.setValue(self.view.outputFileLineEdit.text()))
        self.view.saveAsPushButton.pressed.connect(self._action_save_as)
        self.view.savePushButton.pressed.connect(self._action_save)
        self.view.ticksColorColorButton.colorChanged.connect(self.model.ticks_color.setValue)
        self.view.titleLineEdit.textChanged.connect(self.model.title.setValue)
        self.view.titleColorColorButton.colorChanged.connect(self.model.title_color.setValue)
        self.view.xAxisNameLineEdit.textChanged.connect(self.model.x_axis_name.setValue)
        self.view.xMaxDoubleSpinBox.valueChanged.connect(self.model.x_max.setValue)
        self.view.xMinDoubleSpinBox.valueChanged.connect(self.model.x_min.setValue)
        self.view.yAxisNameLineEdit.textChanged.connect(self.model.y_axis_name.setValue)
        self.view.yMaxDoubleSpinBox.valueChanged.connect(self.model.y_max.setValue)
        self.view.yMinDoubleSpinBox.valueChanged.connect(self.model.y_min.setValue)


    def _set_view_initial_values(self):
        self.view.axesColorColorButton.setColor(self.model.axes_color.value)
        self.view.axesLabelsColorColorButton.setColor(self.model.axes_labels_color.value)
        self.view.backgroundColorColorButton.setColor(self.model.background_color.value)
        self.view.dpiSpinBox.setValue(self.model.dpi.value)
        self.view.figureXDoubleSpinBox.setValue(self.model.figure_x.value)
        self.view.figureYDoubleSpinBox.setValue(self.model.figure_y.value)
        self.view.isShowIntermediateLinesCheckBox.setChecked(self.model.is_show_intermediate_lines.value)
        self.view.isTransparentBackgroundCheckBox.setChecked(self.model.is_transparent_background.value)
        self.view.linesConfigurationTableView.setModel(LinesTableModel(self.model.lines_presets[self.model.lines_preset.value]))
        self.view.linesPresetComboBox.addItems(list(self.model.lines_presets.keys()))
        self.view.linesPresetComboBox.setCurrentIndex(list(self.model.lines_presets.keys()).index(self.model.lines_preset.value))
        self.view.plotPlotWidget.setAxesColor(self.model.axes_color.value)
        self.view.plotPlotWidget.setAxesLabelsColor(self.model.axes_labels_color.value)
        self.view.plotPlotWidget.setBackgroundColor(self.model.background_color.value)
        self.view.plotPlotWidget.setDpi(self.model.dpi.value)
        self.view.plotPlotWidget.setFigureX(self.model.figure_x.value)
        self.view.plotPlotWidget.setFigureY(self.model.figure_y.value)
        self.view.plotPlotWidget.setIsShowIntermediateLines(self.model.is_show_intermediate_lines.value)
        self.view.plotPlotWidget.setIsBackgroundTransparent(self.model.is_transparent_background.value)
        self.view.plotPlotWidget.setTicksColor(self.model.ticks_color.value)
        self.view.plotPlotWidget.setTitle(self.model.title.value)
        self.view.plotPlotWidget.setTitleColor(self.model.title_color.value)
        self.view.plotPlotWidget.setXAxisName(self.model.x_axis_name.value)
        self.view.plotPlotWidget.setXMax(self.model.x_max.value)
        self.view.plotPlotWidget.setXMin(self.model.x_min.value)
        self.view.plotPlotWidget.setYAxisName(self.model.y_axis_name.value)
        self.view.plotPlotWidget.setYMax(self.model.y_max.value)
        self.view.plotPlotWidget.setYMin(self.model.y_min.value)
        self.view.ticksColorColorButton.setColor(self.model.ticks_color.value)
        self.view.titleLineEdit.setText(self.model.title.value)
        self.view.titleColorColorButton.setColor(self.model.title_color.value)
        self.view.xAxisNameLineEdit.setText(self.model.x_axis_name.value)
        self.view.xMaxDoubleSpinBox.setValue(self.model.x_max.value)
        self.view.xMinDoubleSpinBox.setValue(self.model.x_min.value)
        self.view.yAxisNameLineEdit.setText(self.model.y_axis_name.value)
        self.view.yMaxDoubleSpinBox.setValue(self.model.y_max.value)
        self.view.yMinDoubleSpinBox.setValue(self.model.y_min.value)