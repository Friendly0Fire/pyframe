#!/bin/bash

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
cd $SCRIPTPATH

source ~/pyframe.venv/bin/activate

while true
do
    python3 frame.py
    sleep 5
done