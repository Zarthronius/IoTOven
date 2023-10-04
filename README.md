# IoTOven
IoT Smart Oven prototype concept using Raspberry Pi 4

## PROTOTYPE SETUP INSTRUCTIONS
----------------------------

1) Wire components to raspberry pi as shown by PrototypeDiagram.png

2) Start Raspberry Pi

3) Download Oven folder containing the following files
- Adafruit_LCD1602.py (library)
- PCF8574.py (library)
- server.py
- temp_screen_script.py

4) Open the folder

5) Run the following programs:
- server.py
- temp_screen_script.py

==========================

##OPTIONAL
--------

Have programs run automatically at system startup:
NOTE: THE FOLLOWING STEPS ONLY NEEDS TO BE COMPLETED ONCE


1) Open terminal

2) Enter command: sudo nano /etc/rc.local

3) Insert the following text: 
sudo python <FilePath> &
for every python file you wish to run on system startup.
