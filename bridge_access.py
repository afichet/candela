# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets

import phue

from PySide2.QtCore import QObject, Signal, Slot, Property


class BridgeAccess(QObject):
    def __init__(self, ip, user, parent=None):
        super(BridgeAccess, self).__init__(parent)

        self.ip_val = ip
        self.user_val = user

        try:
            self.bridge = phue.Bridge(self.ip_val, self.user_val)
        except phue.PhueRegistrationException as e:
            print("Error connecting to the bridge")

    def __init__(self, parent=None):
        super(BridgeAccess, self).__init__(parent)
        self.ip_val = None
        self.user_val = None

    @Slot()
    def init_connection(self):
        try:
            self.bridge = phue.Bridge(self.ip_val)
            self.bridge.connect()
            self.user = self.bridge.username
            self.connection_established.emit(self.user_val)
        except phue.PhueRegistrationException as e:
            print("Error connecting to the bridge")

    connection_established = Signal(str, name="connection_established")

    def _ip(self):
        return self.ip_val

    def _set_ip(self, v):
        self.ip_val = v

    @Signal
    def ip_changed(self):
        pass

    def _user(self):
        return self.user_val

    def _set_user(self, v):
        self.user_val = v
        if not self.ip_val == None:
            print(self.ip_val, self.user_val)
            self.bridge = phue.Bridge(self.ip, self.user)
            self.bridge.connect()

    @Signal
    def user_changed(self):
        pass

    ip = Property(str, _ip, _set_ip, notify=ip_changed)
    user = Property(str, _user, _set_user, notify=user_changed)