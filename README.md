=========
WoTKit Relay
=========

This is a very simple example of how to receive data from the XBee serial communications
API and relay it to the WoTKit.

This example relies on a zigbee node periodically sending light and temperature readings
from its ADC pins 0 and 1

Installation
============

Install XBee-2.0.0

The following constants need to be configured appropriately for your setup.

APP_KEY = '21083f8935e70e56'
APP_PASSWORD = '15c14931cc27f258'

URL_BASE = 'http://wotkit.sensetecnic.com/wotkit/api/sensors/'
LIGHT_SENSOR = 'office-light'
TEMP_SENSOR = 'office-temp'

Running the Script
==================

Change to the directory containing the code (where this README is)

execute

python wotkit-relay.py

Running the Script at boot
==========================

First create a log file named 'cronlog', in our case we have created it at ```/home/pi/sensors/zigbee-relay/logs/```. 

Then you can add the following line to your crontab via ```sudo crontab -e```, which will boot the

```
@reboot sudo sh /home/pi/sensors/zigbee-relay/runwotkitrelay.sh > /home/pi/sensors/zigbee-relay/logs/cronlog 2>&1 &
```

Dependencies
============

XBee-2.0.0
