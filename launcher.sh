#!/bin/sh

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

ROOT_PATH="/home/pi/watering_system"
MASTER_LOG_PATH="$ROOT_PATH/logs/startlogs"
WORKER_LOG_PATH="$ROOT_PATH/logs/workerlogs"

cd $ROOT_PATH
sleep 10

python3 start.py > $MASTER_LOG_PATH 2>&1 &
python3 worker.py > $WORKER_LOG_PATH 2>&1