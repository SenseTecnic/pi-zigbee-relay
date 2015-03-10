#!/bin sh
cd /home/pi/sensors
#source bin/activate
bin/python zigbee-relay/wotkit-relay.py &
cd /
