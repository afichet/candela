
![256](https://user-images.githubusercontent.com/7930348/85344114-073f6500-b4ef-11ea-9287-ec757b42d9f1.png)
[![Build Status](https://travis-ci.com/afichet/candela.svg?branch=master)](https://travis-ci.com/afichet/candela)

# Candela

Application to control Philips Hue lights.

![home](https://user-images.githubusercontent.com/7930348/85293780-1fd35f00-b49e-11ea-8494-80fe63aacfde.png)

![list](https://user-images.githubusercontent.com/7930348/85293787-2235b900-b49e-11ea-9a14-e3dffd995f1a.png)

# Installation

## Dependencies
This program uses phue and Qt (PySide2).

```
pip3 install phue
pip3 install fbs PySide2
pip3 install requests
pip3 install --upgrade PyInstaller==3.5
```

## Run

```
fbs run
```

## Build

```
fbs freeze
fbs installer
```

Depending on your platform, an installer is created in `target` folder.

# License

This application uses icons from [fontawesome.com](https://fontawesome.com/). See the license there: [https://fontawesome.com/license](https://fontawesome.com/license)
