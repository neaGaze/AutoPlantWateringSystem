#!/usr/bin/python
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1015 as ADS
import busio
import board
import sys
sys.path.insert(1, './mysql')
from mysql_connector import MysqlDriver
from channel import Channel

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Database Connection
db = None

class Calibrator:
    def __init__(self, channel_id):
        self.water_start_threshold = 2.5
        self.water_end_threshold = 2.0
        self.delay = 0
        self.channel = channel_id

def start_db_connection():
    db = MysqlDriver.instance("localhost", "WateringSystem", "nshakya", "plantypi")
    db.connect()

def end_db_connection():
    if db:
        db.disconnect()

start_db_connection()
channel = Channel()

def calibrate(channel_id):
    # setup the right channel based on channel id
    if channel_id == 1:
        channel = AnalogIn(ads, ADS.P0)
    elif channel_id == 2:
        channel = AnalogIn(ads, ADS.P1)
    elif channel_id == 3:
        channel = AnalogIn(ads, ADS.P2)
    elif channel_id == 4:
        channel = AnalogIn(ads, ADS.P3)
    else:
        raise Exception("Invalid channel Id provided. Exiting now\n")
        return
    
    # set up the calibration
    calibrator = Calibrator(channel_id)
    input("Please put your sensor in the dry soil now. Press any key to continue.\n")
    calibrator.water_start_threshold = float(channel.voltage)
    print("The water starting threshold is set at: %s\n" % calibrator.water_start_threshold)
    input("Please water the soil now. Press any key to continue.\n")
    calibrator.water_end_threshold = float(channel.voltage)
    print("The water ending threshold is set at: %s\n" % calibrator.water_end_threshold)
    try:
        calibrator.delay = int(input("Please enter the delay in seconds between the dry soil and watering time.\n"))
    except e:
        print("Looks like you inserted something non integer where it should be an integer. Using the default as 0 secs now.")
        calibrator.delay = 0
    return calibrator


while True:
    sensor_id = input("To calibrate the sensor enter the sensor Id (1/2/3/4) and hit return key.\n")
    try:
        calibrator = calibrate(int(sensor_id))
        
        # TODO assert that the start and end threshold should meet criterias such as the values should always be greater or lower than the other
        channel.update_start_trigger(calibrator.channel, calibrator.water_start_threshold)
        channel.update_end_trigger(calibrator.channel, calibrator.water_end_threshold)
        channel.update_delay(calibrator.channel, calibrator.delay)

        should_continue = input("Press 'Y' or 'y' to continue on calibrate other sensor. \nPress any to exit.\n")
        if should_continue != 'Y'.lower():
            break
    except ex:
        print("Oops! Something went wrong. %s. Exiting now.\n" % ex)
        break

end_db_connection()
