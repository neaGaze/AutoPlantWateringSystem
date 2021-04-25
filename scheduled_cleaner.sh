#!/bin/bash
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

ROOT_PATH="/home/pi/watering_system"
LOG_PATH="$ROOT_PATH/logs/pilogs"
STATUS_LOG_PATH="$ROOT_PATH/logs/system_status.log"

cd $ROOT_PATH

LAUNCHER_PID=`ps aux | egrep "[l]auncher.sh" | awk '{print $2}'`
PROGRAM_PID=`ps aux | egrep "[s]tart.py" | awk '{print $2}'`
NOW=$(date +"%m-%d-%Y %H:%M")

touch $STATUS_LOG_PATH
echo "" > $STATUS_LOG_PATH

if [ -z "$LAUNCHER_PID" ]
then
	echo "$NOW	launcher process is empty" >> $STATUS_LOG_PATH
	if [ -z "$PROGRAM_PID" ]
	then
		echo "$NOW	program is also empty. Nothing to do!" >> $STATUS_LOG_PATH
	else
		echo "$NOW	The program with PID: $PROGRAM_PID is running without launcher. Exiting program now." >> $STATUS_LOG_PATH
	fi

	kill -9 $PROGRAM_PID >/dev/null
	python3 ./cleanup.py > /dev/null

else
	echo "$NOW	launcher process is running with process ID: $LAUNCHER_PID"  >> $STATUS_LOG_PATH
	if [ -z "$PROGRAM_PID" ]
	then
		echo "$NOW	Oops! program with PID: $PROGRAM_PID is not running while launcher is still running. Something is off!" >> $STATUS_LOG_PATH
		kill -9 $PROGRAM_PID >/dev/null
		python3 ./cleanup.py > /dev/null

	else
		echo "$NOW	Looks like both launcher and program ($PROGRAM_PID) are running." >> $STATUS_LOG_PATH
	fi
fi

