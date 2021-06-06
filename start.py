#!/usr/bin/python
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
import RPi.GPIO as GPIO
from adafruit_ads1x15.analog_in import AnalogIn
import sys
sys.path.insert(1, './mysql')
from mysql_connector import MysqlDriver
from activity import Activity
from channel import Channel

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
channels = [AnalogIn(ads, ADS.P0), AnalogIn(ads, ADS.P1), AnalogIn(ads, ADS.P2), AnalogIn(ads, ADS.P3)]

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

# THE GPIO pins currently connected with the raspberry pi
# GPIO | Relay
#--------------
# 26     01
# 19     02
# 13     03
# 06     04
# 12     05
# 16     06
# 20     07
# 21     08
# initiate list with pin gpio pin numbers
gpioList = [6, 13, 19, 26, 12, 16, 20, 21]

# map the water capacitor id with the GPIO pin
sensor_to_gpio = {}
sensor_to_gpio[0] = gpioList[0]
sensor_to_gpio[1] = gpioList[1]
sensor_to_gpio[2] = gpioList[2]
sensor_to_gpio[3] = gpioList[3]

GPIO.setmode(GPIO.BCM)

# Initialize all relay gates to be open or HIGH
for i in gpioList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

water_start_threshold = 2.5
#water_end_threshold = 2.0
water_end_threshold = 2.0

pipe_lock = -1

print("Channel {}\t{:>5}\t{:>5}".format('Channel', 'raw', 'v'))

# Starting database connection
db = MysqlDriver.instance("localhost", "WateringSystem", "nshakya", "plantypi")
db.connect()
activity = Activity()
db_channel = Channel()
thresholds = {}
for i,c in enumerate(channels):
    channel_id = i + 1
    thresholds[channel_id] = db_channel.read_start_trigger(channel_id)
print("water thresholds: %s \n" % (thresholds))

try:
    while True:
        open_channels = activity.read_are_open()
        print("OPEN channels: %s" % open_channels)

        for i,chan in enumerate(channels):
            try:
                print("{}\t{:>5}\t{:>5.3f}".format(i, chan.value, chan.voltage))
            except:
                print("Error! Something went wrong with the printing process")
            finally:
                """
                if pipe_lock >= 0:
                    if pipe_lock == i and float(chan.voltage) <= water_end_threshold:
                        GPIO.output(sensor_to_gpio[i], GPIO.HIGH)
                        pipe_lock = -1
                        print("UNLOCKING PIPE %d" % i)
                elif float(chan.voltage) >= water_start_threshold:
                    pipe_lock = i
                    print("LOCKING PIPE %d" % i)
                    GPIO.output(sensor_to_gpio[i], GPIO.LOW)
                """
                channel_id = i+1
                if channel_id not in open_channels and float(chan.voltage) >= thresholds[channel_id]:
                    activity.insert_water_start_txn(channel_id)
        time.sleep(2)
except KeyboardInterrupt:
    print("Quit")
    db.disconnect()
    GPIO.cleanup()
