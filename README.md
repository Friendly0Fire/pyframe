# PiFrame: A simple photo frame for the Raspberry Pi

PiFrame is a simple Python-based photo frame which loads pictures from a Samba share and displays them with smart title generation. In addition, if the connected monitor is HDMI-CEC compliant, it will automatically be turned off at night and back on during the day.

## Installation

Execute `install.sh` passing the full Samba share containing the pictures as the sole argument.

### If using a window manager

To further clean up the desktop and create a seamless experience, hide most desktop elements as follows (instructions for lightdm with Raspberry Pi Desktop):
* Edit `/etc/xdg/lxsession/LXDE-pi/autostart`
* To hide the top bar, prepend `#` to the line which starts with `@lxpanel`
* To hide the cursor, append the following line: `@unclutter -display :0 -idle 3 -root -noevents`

It is recommended to disable the screensaver by placing an empty file named `.xscreensaver` in `$HOME`.

### If only using a display manager

Simply run `init.sh` from your `.xsession` file.

### Pi-specific guide

A Raspberry Pi 3B or better can very easily run this photo frame and is ideally suited thanks to its low cost and small size.

The recommended installation is to start off the *lite* OS image, which you can install via the Raspberry Pi Imager onto a microSD card. From there, manually install X11 and lightdm via the package manager:
```
sudo apt-get install --no-install-recommends xserver-xorg-video-all xserver-xorg-input-all xserver-xorg-core xinit x11-xserver-utils lightdm
```
 and enable GUI autologin through `raspi-config`.

 It is also recommended to enable "Network at boot" in `raspi-config` in order to make sure the Samba share mounting succeeds.