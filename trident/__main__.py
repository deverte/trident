"""
Trident is a program with graphical user interface for transforming singlet
absorption lines to triplets and visualizing them.
Compatible file format for parsing (commonly named as "Absorption.dat"):
    VV FullAbs ResPart Thermal
    <float> <float> <float> <float>
    <...> <...> <...> <...>

Development notes:
    Application architecture based on "MVP Passive View" pattern with some
    extensions (model <-> presenter <-> view bindings) due to Qt's signals/slots
    abilities.
    Model is described at model/model.py file.
    View is described at ui/.../view.py files (corresponding to each widget).
    Presenter is described at ui/.../presenter.py files (corresponding to each
    widget, if needed).

Author: Artem Shepelin
License: GPLv3
Repository: https://github.com/deverte/gleipnir
"""

import sys

from PyQt6.QtWidgets import QApplication

from trident.model.model import Model
from trident.ui.presenter import MainWindowPresenter
from trident.ui.view import MainWindow


def main():
    app = QApplication(sys.argv)

    model = Model()
    view = MainWindow()
    presenter = MainWindowPresenter(model, view)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()