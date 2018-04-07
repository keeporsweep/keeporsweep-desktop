<p align="center">
    <img src="https://raw.githubusercontent.com/keeporsweep/keeporsweep-desktop/master/images/icon-256.png" height="128">
</p>
<h3 align="center"><a href="http://keeporsweep.net" target="_blank">Keep or Sweep</a></h3>
<p align="center">Randomly clean data off your computer!<p>
<p align="center">
    <img src="https://raw.githubusercontent.com/keeporsweep/keeporsweep-desktop/master/images/screenshot.png" height="500">
</p>



## Install

This is the desktop app (v0.1.0) for [⊞Windows](https://github.com/keeporsweep/keeporsweep-desktop/releases/download/v0.1.0/Keep-or-Sweep.exe), [🍏macOS](https://github.com/keeporsweep/keeporsweep-desktop/releases/download/v0.1.0/Keep-or-Sweep.app.zip) & [🐧Linux](https://github.com/keeporsweep/keeporsweep-desktop/releases/download/v0.1.0/Keep-or-Sweep-Linux.Sweep).

There’s also a [☁️Nextcloud app](https://github.com/keeporsweep/keeporsweep), and more info at [🔀keeporsweep.net](http://keeporsweep.net).



## Contribute

Contributions are always welcome! 😍 Check out the [list of issues](https://github.com/keeporsweep/keeporsweep-desktop/issues) and see what you like to contribute. Keep or Sweep is written in 🐍Python so if you know about that – come on board!


### Development setup

1. Install the dependencies: We need [Pillow](https://pillow.readthedocs.io/en/latest/installation.html) (Python library for image handling) and [Send2Trash](https://github.com/hsoft/send2trash) (to move files to trash cross-platform instead of permanently removing them). Type these commands in a terminal window:
```
sudo easy_install pip
pip3 install Pillow
pip3 install Send2Trash
```
2. Make `keeporsweep.py` executable by right-click → Properties → Allow executing file as program. (Or in the terminal with `chmod +x keeporsweep.py`)
3. Then place `keeporsweep.py` in any folder and click it! 🎉 (Or in the terminal run `python3 keeporsweep.py`)


### Building an executable app

1. Install [PyInstaller](https://www.pyinstaller.org/) via terminal:
```
pip3 install pyinstaller
```
2. Then use this command to build the application for your operating system (use icon.icns instead of icon.ico when building on macOS):
```
pyinstaller --name="Keep or Sweep" --onefile --noconsole --icon="images/icon.ico" --clean keeporsweep.py
```
3. The executable file will be in the `dist` subfolder.

In case the icon was changed, we need to generate those again. Windows .ico uses the 256px icon and can be saved using [GIMP](https://www.gimp.org/), macOS .icns uses icons ranging from 16px to 1024px and can be generated using [png2icns](https://dentrassi.de/2014/02/25/creating-mac-os-x-icons-icns-on-linux/).
