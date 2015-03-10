#! /usr/bin/python

"""
wotkit-relay.py

By Mike Blackstock 2012
Based on sample code from Paul Malmsten, 2010
pmalmsten@gmail.com

This example continuously reads the serial port and processes IO data
received from a remote XBee, then sends it to the wotkit.
"""
import urllib
import urllib2
import base64

from xbee import ZigBee
import serial

#zigbee explorer communications
PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

#credentials for sending data to wotkit
#APP_KEY = 'd4b7259dfe84dc27'
#APP_PASSWORD = '07a4edeffff644e1'
APP_KEY = '36d3ad7c43332de2'
APP_PASSWORD = '87838f58bbe74ba9'


#wotkit URL and sensors used.
URL_BASE = 'http://wotkit.sensetecnic.com/api/v2/sensors/'
LIGHT_SENSOR = 'sensetecnic.demo-zigbee-light'
TEMP_SENSOR = 'sensetecnic.demo-zigbee-temperature'

# Open serial port
ser = serial.Serial(PORT, BAUD_RATE)

# Create API object
xbee = ZigBee(ser)

# Set up the HTTP request for the wotkit
# this is our app key and password, for all of my home sensors
base64string = base64.encodestring('%s:%s' % (APP_KEY, APP_PASSWORD))[:-1]

headers = {
    'User-Agent': 'httplib',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': "Basic %s" % base64string
}

# Continuously read and send data to the wotkit as soon as they arrive.
while True:
    try:
        response = xbee.wait_read_frame()
        print response
        # get the light level (adc-0) and temp (adc-1)
        lightLevel = 1023-response["samples"][0]["adc-0"]
        temp = response["samples"][0]["adc-1"]
        #convert to degrees celcius
        temp = (3.0*temp*100)/(1024*3.2/1.2)
        tempC = (temp-32)*5/9

        print lightLevel
        print temp, tempC

        # send light to wotkit
        
        datafields = [('value','%f' % lightLevel)]
        params = urllib.urlencode(datafields)
        req = urllib2.Request(URL_BASE+LIGHT_SENSOR+"/data",params,headers)
        try:
            result = urllib2.urlopen(req)
        
        except urllib2.URLError, e:
            print "error", e

        # send temperature
        
        datafields = [('value','%f' % tempC)]
        params = urllib.urlencode(datafields)
        req = urllib2.Request(URL_BASE+TEMP_SENSOR+"/data",params,headers)
        try:
            result = urllib2.urlopen(req)
        
        except urllib2.URLError, e:
            print "error", e           

    except KeyboardInterrupt:
        break
        
ser.close()
