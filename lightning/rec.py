#!/usr/bin/python
# -*- coding: utf-8 -*- 

from RPi_AS3935 import RPi_AS3935
import RPi.GPIO as GPIO
import time
import csv
from datetime import datetime
import requests
import sys

LED = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, True)

# Rev. 1 Raspberry Piの場合は bus=0,  rev. 2 の場合はbus=1
# 秋月製の雷センサーはI2Cアドレスは0x00固定

sensor = RPi_AS3935(address=0x00, bus=1)
sensor.reset() 
sensor.set_indoors(False)
sensor.set_noise_floor(0)
#(5) 32pF チューニングの結果をここで指定する
sensor.calibrate(tun_cap=0x05)

filename = '/root/lightning/' + datetime.now().strftime("%Y-%m-%d") + '.lightning.txt'

def handle_interrupt(channel):
	time.sleep(0.003)
	global sensor
	reason = sensor.get_interrupt()
	now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	outputfile = open(filename , "a" )
	writer = csv.writer(outputfile)
	if reason == 0x01:
		sensor.raise_noise_floor()
		buffer = [now, "Noise level too high"]
		print (buffer)
		writer.writerow(buffer)
	elif reason == 0x04:
		sensor.set_mask_disturber(True)
		buffer = [now, "Disturber detected"]
		print (buffer)
		writer.writerow(buffer)
	elif reason == 0x08:
               	GPIO.output(LED, True)
		distance = sensor.get_distance()
		energy = sensor.get_energy()
		buffer = [now, "lightning!" ,  str(distance)  , str(energy)]
		print (buffer)
		writer.writerow(buffer)
                url = "http://labs.weathernews.jp/hack/lightning/ingest.cgi?id=ltng1001&distance=" + str(distance)  + "&energy=" + str(energy)
                print (url)
                resp = requests.get(url)
	outputfile.close()

#ここから始まり
IRQ = 17

GPIO.setup(IRQ, GPIO.IN)
GPIO.add_event_detect(IRQ, GPIO.RISING, callback=handle_interrupt)
now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

outputfile = open(filename, "a")
writer = csv.writer(outputfile)
distance = sensor.get_distance()
energy = sensor.get_energy()
buffer = [now, "Waiting for lightning",  str(distance)  , str(energy) ]
print (buffer)
writer.writerow(buffer)
outputfile.close()

while True:
	time.sleep(1.0)
	GPIO.output(LED, False)
