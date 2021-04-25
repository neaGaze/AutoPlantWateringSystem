#!/usr/bin/python
import RPi.GPIO as GPIO

gpioList = [6, 13, 19, 26, 12, 16, 20, 21]
GPIO.setmode(GPIO.BCM)
for i in gpioList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)
GPIO.cleanup()
