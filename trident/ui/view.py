"""
MainWindow is a view class for application main window.
It loads and shows form designed in Qt Designer.

Author: Artem Shepelin
License: GPLv3
"""

import os

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from trident.ui.color_button.view import ColorButton # uic promotion (required for pyinstaller)
from trident.ui.file_line_edit.view import FileLineEdit # uic promotion (required for pyinstaller)
from trident.ui.plot_widget.view import PlotWidget # uic promotion (required for pyinstaller)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(os.path.join(os.path.dirname(__file__), "main.ui"), self)

        theme_file = os.path.join(os.path.dirname(__file__), "dark_theme.qss")
        if os.path.exists(theme_file):
            self.setStyleSheet(open(theme_file, "r").read())

        self.show()