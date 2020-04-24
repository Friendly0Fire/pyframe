#!/bin/sh

# Python
sudo apt install python3
pip3 install -r requirements.txt

# Crontab setup
crontab -l > cron.tmp
echo "* * * * * python3 ~/share/Cadre/cadre.py > ~/share/Cadre/cadre.log 2>&1" >> cron.tmp
echo "* * * * * python3 ~/share/Cadre/cadre.py > ~/share/Cadre/cadre.log 2>&1" >> cron.tmp
echo "30 23 * * * xset dpms force off" >> cron.tmp
echo "0 8 * * * xset dpms force on" >> cron.tmp
crontab cron.tmp
rm cron.tmp

sudo mount -o rw,remount /boot
sudo echo "hdmi_blanking=1" >> /boot/config.txt
sudo mount -o ro,remount /boot

sudo shutdown -r now