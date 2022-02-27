"""
Table Model for work with absorption lines configuration.

Author: Artem Shepelin
License: GPLv3
"""

from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtCore import Qt
DisplayRole = Qt.ItemDataRole.DisplayRole
Horizontal = Qt.Orientation.Horizontal


class LinesTableModel(QAbstractTableModel):
    def __init__(self, preset):
        super().__init__()

        self._preset = preset


    def data(self, index, role):
        if role == DisplayRole:
            column = ["shifts", "coefficients"][index.column()]
            return self._preset[column][index.row()]


    def headerData(self, section, orientation, role):
        if role == DisplayRole:
            if orientation == Horizontal:
                if section == 0:
                    return "shifts"
                if section == 1:
                    return "coefficients"


    def rowCount(self, index):
        return len(self._preset["coefficients"])


    def columnCount(self, index):
        return 2