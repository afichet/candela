# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtQml import qmlRegisterType

from app_config import AppConfig
from bridge_model import BridgeModel
from bridge_access import BridgeAccess
from light_model import LightModel

if __name__ == '__main__':
    sys_argv = sys.argv
    sys_argv += ['--style', 'material']

    app = QGuiApplication(sys_argv)

    qmlRegisterType(AppConfig, 'AppConfig', 1, 0, 'AppConfig')
    qmlRegisterType(BridgeModel, 'BridgeModel', 1, 0, 'BridgeModel')
    qmlRegisterType(BridgeAccess, 'BridgeAccess', 1, 0, 'BridgeAccess')
    qmlRegisterType(LightModel, 'LightModel', 1, 0, 'LightModel')

    app_config = AppConfig()
    bridges = BridgeModel(app_config)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("app_config", app_config)
    engine.rootContext().setContextProperty("bridge_model", bridges)
    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
