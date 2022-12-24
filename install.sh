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
sudo apt -y install python3 python3-pip cifs-utils freeglut3-dev cec-utils
sudo pip3 install -r requirements.txt

sudo mkdir -p /mnt/photos
if grep -q -F $1 /etc/fstab; then
    echo "Mount entry for $1 already exists, skipping..."
else
    sudo su -c "echo '$1 /mnt/photos    cifs    ro,noexec,user=nobody,guest 0 0' >> /etc/fstab"
fi

cp .xscreensaver ~/.xscreensaver