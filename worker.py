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
from datetime import datetime

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
channels = [AnalogIn(ads, ADS.P0), AnalogIn(ads, ADS.P1), AnalogIn(ads, ADS.P2), AnalogIn(ads, ADS.P3)]

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

# Starting database connection
db = MysqlDriver.instance("localhost", "WateringSystem", "nshakya", "plantypi")
db.connect()
activity = Activity()
db_channel = Channel()
thresholds = {}
for i,c in enumerate(channels):
    channel_id = i + 1
    thresholds[channel_id] = {
        'end': db_channel.read_end_trigger(channel_id)
    }

"""
Checks to see if the sensor is dry/wet and/or the pump is running longer than 20 secs 
"""
def is_wet_or_timeout(sensor_msrmnt, water_end_msrmnt):
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() <= 20:
        if sensor_msrmnt <= water_end_msrmnt: # if not dry
            return True
        time.sleep(2)
    return True

# Run a forever loop to check the dryness    
try:
    while True:
        open_channels_with_txnid = activity.read_are_open_with_txnid()
        print("OPEN channels w/t txnid: %s" % open_channels_with_txnid)
        open_channels = list(map(lambda x: x[0], open_channels_with_txnid))
        txn_ids = list(map(lambda x: x[1], open_channels_with_txnid))
        channel_to_txn_id = {}
        for i, c_id in enumerate(open_channels):
            channel_to_txn_id[c_id] = txn_ids[i]
        print("OPEN channels: %s" % open_channels)

        for i,chan in enumerate(channels):
            try:
                print("{}\t{:>5}\t{:>5.3f}".format(i, chan.value, chan.voltage))
            except:
                print("Error! Something went wrong with the printing process")
            finally:
                channel_id = i+1
                if channel_id in open_channels:
                    GPIO.output(sensor_to_gpio[i], GPIO.LOW)    # open the water pump
                    print("STARTING WATER PUMP on channel %d NOW..." % channel_id)
                    if is_wet_or_timeout(round(float(chan.voltage), 1), round(thresholds[channel_id]['end'], 1)):
                        GPIO.output(sensor_to_gpio[i], GPIO.HIGH)   # close the water pump
                        activity.insert_water_end_txn(channel_id, channel_to_txn_id[channel_id])
                        print("ENDING WATER PUMP on channel %d NOW." % channel_id)
            time.sleep(2)
        time.sleep(20)
        
except KeyboardInterrupt:
    print("Quit")
    db.disconnect()
    GPIO.cleanup()
