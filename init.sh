#!/bin/bash
sleep 10
while ! ping -c 1 -W 1 8.8.8.8; do sleep 1; done;

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
cd $SCRIPTPATH

sudo mount -a
python3 frame.py