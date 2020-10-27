#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ "$#" -ne 1 ]; then
    echo "Please provide the SAMBA share path as an argument (no spaces in path)."
    exit 1
fi

if [[ $1 =~ "\\" ]]; then
    echo "Please use /'s rather than \\'s in your SAMBA share path."
    exit 1
fi

# Python
sudo apt -y install python3 python3-pip cifs-utils freeglut3-dev unclutter xscreensaver cec-utils
sudo pip3 install -r requirements.txt

CRONENTRY="* * * * * $DIR/init.sh"

# Crontab setup
crontab -l > cron.tmp
if ! grep -q $CRONENTRY cron.tmp; then
    echo $CRONENTRY >> cron.tmp
else
    echo "Cron entry already exists, skipping..."
fi
crontab cron.tmp
rm cron.tmp

sudo mkdir -p /mnt/photos
if ! grep -q $1 /etc/fstab; then
    sudo su -c "echo '$1 /mnt/photos    cifs    ro,noexec,user=nobody,guest 0 0' >> /etc/fstab"
else
    echo "Mount entry for $1 already exists, skipping..."
fi