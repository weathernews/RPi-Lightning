#!/usr/bin/python
from RPi_AS3935 import RPi_AS3935
##Developed by  Phil merlinmb. Revised by Hiroshi Ishikawa.

import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)

sensor = RPi_AS3935(address=0x00, bus=1)

sensor.reset() 
print "set indoors"
sensor.set_indoors(True)
print "set noise floor to 0"
sensor.set_noise_floor(0)

sensor.read_data()
print "register0x08= ",bin(sensor.registers[0x08])

print "set register to get resonant frequency"

sensor.set_disp_lco(True)
print "!! Measure IRQ for freq (x16)"

sensor.read_data()
print "register0x08= ",bin(sensor.registers[0x08])

print "set tune cap, 15 second intervals (measure)"
for x in range(0, 16):
	print x
	sensor.calibrate(tun_cap=x)
	time.sleep(15.0)

time.sleep(5.0)
sensor.set_disp_lco(False)
print "register0x08= ",bin(sensor.registers[0x08])

