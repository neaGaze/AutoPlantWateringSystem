#!/usr/bin/python
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
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
                channel_id = i+1
                if channel_id not in open_channels and round(float(chan.voltage), 1) >= round(thresholds[channel_id], 1):
                    activity.insert_water_start_txn(channel_id)
        time.sleep(2)
except KeyboardInterrupt:
    print("Quit")
    db.disconnect()
