#!/bin/sh

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

ROOT_PATH="/home/pi/watering_system"
LOG_PATH="$ROOT_PATH/logs/pilogs"

cd $ROOT_PATH
sleep 10

python3 start.py > $LOG_PATH 2>&1
