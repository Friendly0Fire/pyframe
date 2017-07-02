#!/bin/bash
sleep 10
while ! ping -c 1 -W 1 8.8.8.8; do sleep 1; done;

# Absolute path to this script. /home/user/bin/foo.sh
SCRIPT=$(readlink -f $0)
# Absolute path this script is in. /home/user/bin
SCRIPTPATH=`dirname $SCRIPT`
cd $SCRIPTPATH

sudo mount -a
python3 cadre.py