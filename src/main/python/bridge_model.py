# This Python file uses the following encoding: utf-8
#from PySide2.QtCore import QAbstractItemModel, QModelIndex, QVariant
from PySide2.QtCore import QAbstractListModel
from PySide2.QtCore import QModelIndex
from PySide2.QtCore import Qt

from app_config import AppConfig


class BridgeModel(QAbstractListModel):
    def __init__(self, config, parent=None):
        super(BridgeModel, self).__init__(parent)
        self.config = config

    def index(self, row, column, parent=QModelIndex):
        return self.createIndex(row, column, parent)

    def parent(self, index):
        return self.createIndex()

    def rowCount(self, parent=QModelIndex):
        return len(self.config.all_bridges)

    def columnCount(self, parent=QModelIndex):
        return 1

    def data(self, index, role):
        key = self.roleNames()[role]
        return self.config.all_bridges[index.row()][key.decode('utf-8')]

    def roleNames(self):
        return {
            Qt.UserRole + 1: b'ip',
            Qt.UserRole + 2: b'user',
            Qt.UserRole + 3: b'configured'}
