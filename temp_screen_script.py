# Author: W20016567

## Imports
import os                                       # OS functionality
from time import sleep

#LIBRARIES BY FREENOVE
#https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/blob/master/Code/Python_Code/20.1.1_I2CLCD1602/Adafruit_LCD1602.py
from PCF8574 import PCF8574_GPIO                # Module for I2C GPIO functions
from Adafruit_LCD1602 import Adafruit_CharLCD   # Module for screen1602 operations (e.g. clear/display contents)


## I2C Addresses
                                                # PCF8574 AND PCF8574A are functionally similar, but occupy different address spaces
PCF8574addr = 0x20                              # PCF8574 chip I2C address. Can be addressed from 0x20 to 0x27
PCF8574Aaddr = 0x38                             # PCF8574A chip I2C address. Can be addressed from 0x38 to 0x3F

## Methods
def sensors():
    devices = []                                # Initialise empty list
    for i in os.listdir('/sys/bus/w1/devices'): # Iterate devices list
        if i != 'w1_bus_master1':               # If sensor device
            devices.append(i)                   # Append to devices list
    return devices                              # Return devices list

# Get Temperature
def read(ds18b20):
    location = '/sys/bus/w1/devices/' + ds18b20 + '/temperature' # Sensor data file path
    tfile = open(location)                                       # Opens file
    text = tfile.read()                                          # Reads file
    tfile.close()                                                # Closes file
    
    temperature = float(text)       # Converts temperature string to float
    celsius = temperature / 1000    # Convert to celsius
    return celsius
        
# Return Temperature
def read_disp(ds18b20):
    try:
        return(read(ds18b20))
    except:
        return('Error')

# Display and refresh Temperature on screen
def display(serialNums):
    expansionBoard.output(3,1)         # Turn on screen backlight
    screen.begin(16,2)                 # Set number of screen lines (16) and columns (2)
    sensorNames = ['Probe','Oven']     # Names for each temperature sensor
    
    
    while(True):        
        sensorNamesIndex = 0
        screen.clear()                                                                      # Clear screen
        screen.setCursor(0,0)                                                               # Set cursor position
        
        for i in serialNums:                                                                # Iterate over both sensors
            screen.message('%s: %0.3f C\n' % (sensorNames[sensorNamesIndex], read_disp(i))) # Display formatted sensor data on screen 
            sensorNamesIndex += 1
        sleep(2)                                                                            # 2 second sleep before repeat


## Setup
while True:
    try:                                                                                      # Try to create PCF8574 GPIO adapter.
        expansionBoard = PCF8574_GPIO(PCF8574addr)
        screen = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=expansionBoard)  # GPIO adapter used to create screen.
    except:                                                                                   # Keep retrying in case of error                         
        continue
    break

## Main
if __name__ == '__main__':
    try:
        screen.clear()              # Clear screen
        serialNums = sensors()      # Get serial numbers for each temperature sensor
        display(serialNums)         # Display sensor data on screen

    except KeyboardInterrupt:       # Quit program on interrupt
        screen.clear()
        quit()
