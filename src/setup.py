from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(include_files = [
    'main.qml',
    'BridgeView.qml',
    'LightControl.qml',
    'PairBridge.qml',
    'icons/',
    'icons.qrc',
    'view.qrc'], packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, targetName = 'Candela')
]

setup(name='Candela',
      version = '0.1',
      description = 'Application to control Philips Hue lights',
      options = dict(build_exe = buildOptions),
      executables = executables)
