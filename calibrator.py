#!/usr/bin/python
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1015 as ADS

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

class Calibrator:
    def __init__(self, channel_id):
        self.water_start_threshold = 2.5
        self.water_end_threshold = 2.0
        self.channel = channel_id

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
        raise Exception("Invalid channel Id provided. Exiting now")
        return
    
    # set up the calibration
    calibrator = Calibrator(channel_id)
    input("Please put your sensor in the soil now. Press any key to continue.")
    calibrator.water_start_threshold = float(chan.voltage)
    input("Please pull your sensor out from the soil now. Press any key to continue.")
    calibrator.water_end_threshold = float(chan.voltage)

while True:
    sensor_id = input("To calibrate the sensor enter the sensor Id (1/2/3/4) and hit return key")
    try:
        calibrate(sensor_id)
        should_continue = input("Press 'Y' or 'y' to continue on calibrate other sensor. \nPress any to exit.")
        if should_continue != 'Y'.lower():
            break
    except ex:
        print("Oops! Something went wrong. %s. Exiting now." % ex)
        break
