# PyFrame: A simple photo frame made in Python

PyFrame is a simple Python-based photo frame which loads pictures from a Samba share and displays them with smart title generation. In addition, if the connected monitor is HDMI-CEC compliant, it will automatically be turned off at night and back on during the day.

## Installation

Install prerequisites:
```
sudo apt -y install python3 python3-pip python3-venv cifs-utils freeglut3-dev cec-utils libcec-dev
```

Install python packages from `requirements.txt`. A virtual environment is recommended, e.g.,
```
python3 -m venv ~/pyframe.venv
source ~/pyframe.venv/bin/activate
pip3 install -r requirements.txt
```

### Handling pictures location

By default, PyFrame expects the photos to be stored on a remote file server and mounted to `/mnt/photos`. If the files are stored locally, you can simply edit your configuration to point to the correct location.

As an example, to automatically mount a SMB share to `/mnt/photos` on boot, you can run:
```
sudo su -c "echo '<your file share here> /mnt/photos    cifs    ro,noexec,noserverino,user=nobody,guest 0 0' >> /etc/fstab"
```
making sure your file share uses forward slashes `/`, e.g. a share at `\\server\photos` would be entered as `//server/photos`.

### If using a window manager

To further clean up the desktop and create a seamless experience, hide most desktop elements as follows (instructions for lightdm with Raspberry Pi Desktop):
* Edit `/etc/xdg/lxsession/LXDE-pi/autostart`
* To hide the top bar, prepend `#` to the line which starts with `@lxpanel`
* To hide the cursor, append the following line: `@unclutter -display :0 -idle 3 -root -noevents`

It is recommended to disable the screensaver by placing an empty file named `.xscreensaver` in `$HOME`.

### If only using a display manager

Simply run `init.sh` from your `.xsession` file.

### If starting from a clean slate without a display manager

You can install the bare minimum X server with:
```
sudo apt-get install xserver-xorg-core xinit --no-install-recommends --no-install-suggests
```

### Pi-specific guide

A Raspberry Pi 3B or better can very easily run this photo frame and is well suited thanks to its low cost and small size.

The recommended installation is to start off the *lite* OS image, which you can install via the Raspberry Pi Imager onto a microSD card. From there, manually install X11 and lightdm via the package manager:
```
sudo apt-get install --no-install-recommends xserver-xorg-video-all xserver-xorg-input-all xserver-xorg-core xinit x11-xserver-utils lightdm
```
 and enable GUI autologin through `raspi-config`.

It is also recommended to enable "Network at boot" in `raspi-config` in order to make sure the Samba share mounting succeeds.

To disable the screensaver, the recommended approach is to edit `/etc/lightdm/lightdm.conf`, look for the line `#xserver-command=X` and change it to `xserver-command=X -s 0 -dpms -s noblank`, which disables screen timeout, disables display power management services, and disables blanking. Note that this will not affect PyFrame's ability to turn off the screen at night, which uses HDMI-CEC instead. If your screen does not support CEC, this may cause the screen to never sleep.