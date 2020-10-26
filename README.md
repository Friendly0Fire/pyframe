# PiFrame: A simple photo frame for the Raspberry Pi

PiFrame is a simple Python-based photo frame which loads pictures from a Samba share and displays them with smart title generation. In addition, if the connected monitor is HDMI-CEC compliant, it will automatically be turned off at night and back on during the day.

## Installation

Execute `install.sh` passing the full Samba share containing the pictures as the sole argument.

To further clean up the desktop and create a seamless experience, hide most desktop elements as follows (instructions for lightdm with Raspberry Pi Desktop):
* Edit `/etc/xdg/lxsession/LXDE-pi/autostart`
* To hide the top bar, prepend `#` to the line which starts with `@lxpanel`
* To hide the cursor, append the following line: `@unclutter -display :0 -idle 3 -root -noevents`

It is recommended to disable the screensaver by placing an empty file named `.xscreensaver` in `$HOME`.
