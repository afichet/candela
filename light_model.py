# This Python file uses the following encoding: utf-8

from PySide2.QtCore import Qt
from PySide2.QtCore import QAbstractListModel
from PySide2.QtCore import QModelIndex
from PySide2.QtCore import Slot
from PySide2.QtCore import Signal
from PySide2.QtCore import Property

from bridge_access import BridgeAccess

import phue


# Colour utility functions


def clamp(v, a=0, b=1):
    return min(max(v, a), b)


def xy_rgb(xy, brightness):
    Y = brightness / 255
    x, y = xy

    d = Y / y
    X = x * d
    Z = (1 - x - y) * d

    R =  3.24096994 * X - 1.53738318 * Y - 0.49861076 * Z
    G = -0.96924364 * X + 1.8759675  * Y + 0.04155506 * Z
    B =  0.05563008 * X - 0.20397696 * Y + 1.05697151 * Z

    c = [R, G, B]

    # sRGB gamma correction
    c = [12.92 * v if v <= 0.0031308 else (1.055 * pow(v, 1./2.4) - 0.055) for v in c]

    return [int(255 * clamp(v)) for v in c]


def rgb_xy(r, g, b):
    c = [r, g, b]
    c = [v/255 for v in c]

    # To linear
    c = [v/12.92 if v <= 0.04045 else pow((v + 0.055)/1.055, 2.4) for v in c]

    R, G, B = c

    X = 0.41239080 * R + 0.35758434 * G + 0.18048079 * B
    Y = 0.21263901 * R + 0.71516868 * G + 0.07219232 * B
    Z = 0.01933082 * R + 0.11919478 * G + 0.95053215 * B

    s = X + Y + Z
    x = X / s
    y = Y / s

    return (x, y), int(clamp(255 * Y, 0, 255))


class LightModel(QAbstractListModel):
    n_lights = 0

    def __init__(self, parent=None):
        super(LightModel, self).__init__(parent)
        self.bridge_val = None
        self.user_val = None
        self.ip_val = None

    @Slot()
    def update(self):
        self.dataChanged.emit(
            self.createIndex(0, 0),
            self.createIndex(self.n_lights, 1))

    def index(self, row, column, parent=QModelIndex):
        return self.createIndex(row, column, parent)

    def parent(self, index):
        return self.createIndex()

    def rowCount(self, parent=QModelIndex):
        if self.bridge is None:
            self.n_lights = 0

        self.n_lights = len(self.bridge.lights)

        return self.n_lights

    def data(self, index, role):
        key = self.roleNames()[role]
        light = self.bridge.lights[index.row()]

        if key == b'id':
            return index.row()
        elif key == b'name':
            return light.name
        elif key == b'on':
            return light.on
        elif key == b'colour':
            R, G, B = xy_rgb(light.xy, light.brightness)
            return "#{0:02x}{1:02x}{2:02x}".format(R, G, B)
        elif key == b'brightness':
            return light.brightness/255

    def roleNames(self):
        return {
            Qt.UserRole + 1: b'id',
            Qt.UserRole + 2: b'name',
            Qt.UserRole + 3: b'on',
            Qt.UserRole + 4: b'colour',
            Qt.UserRole + 5: b'brightness'}

    def _connect(self):
        if self.ip_val is not None and self.user_val is not None:
            self.bridge = phue.Bridge(self.ip, self.user)
            self.bridge.connect()

    def _ip(self):
        return self.ip_val

    def _set_ip(self, v):
        self.ip_val = v
        self._connect()

    @Signal
    def ip_changed(self):
        pass

    def _user(self):
        return self.user_val

    def _set_user(self, v):
        self.user_val = v
        self._connect()

    @Signal
    def user_changed(self):
        pass

    @Slot(int, bool)
    def change_state(self, id, new_state):
        self.bridge.lights[id].on = new_state

    @Slot(int, str)
    def change_color(self, id, color):
        if color == '#000000':
            return

        hexa = color.lstrip('#')

        R, G, B = tuple(int(hexa[i:i+2], 16) for i in (0, 2, 4))
        xy, Y = rgb_xy(R, G, B)

        self.bridge.lights[id].xy = xy
        self.bridge.lights[id].brightness = Y

#        self.dataChanged.emit(
#            self.createIndex(id, 0),
#            self.createIndex(id+1, 1))

    @Slot(int, float)
    def set_brightness(self, id, brightness):
        self.bridge.lights[id].brightness = int(brightness * 255)
#        self.dataChanged.emit(
#            self.createIndex(id, 0),
#            self.createIndex(id+1, 1))

    ip = Property(str, _ip, _set_ip, notify=ip_changed)
    user = Property(str, _user, _set_user, notify=user_changed)
