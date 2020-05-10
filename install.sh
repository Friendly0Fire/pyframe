#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ "$#" -ne 1 ]; then
    echo "Please provide the SAMBA share path as an argument (no spaces in path)."
    exit 1
fi

# Python
sudo apt install python3 python3-pip cifs-utils freeglut3-dev unclutter xscreensaver
sudo pip3 install -r requirements.txt

# Crontab setup
crontab -l > cron.tmp
echo "* * * * * python3 $DIR/cadre.py > $DIR/cadre.log 2>&1" >> cron.tmp
crontab cron.tmp
rm cron.tmp

sudo mkdir /mnt/photos
sudo su -c "echo '$1 /mnt/photos cifs _netdev,username=root,password=,dir_mode=0755,uid=500,gid=500 0 0' >> /etc/fstab"