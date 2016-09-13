#!/usr/bin/python
# -*- coding: utf-8 -*-
# http://www.ishikawa-lab.com/RasPi_lightning.html
# 問い合わせ先：株式会社ウェザニューズ
# http://weathernews.jp/c/contact.html

from RPi_AS3935 import RPi_AS3935
import RPi.GPIO as GPIO
import time
import csv
from datetime import datetime
import requests
import sys
import os
import os.path
mypath = os.path.dirname(sys.argv[0])
if mypath == "":
        mypath = "."
else:
        sys.path.append(mypath)
from id import serial_number        

RST = 21        # リセット端子
LED = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(RST, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
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

if not os.path.exists(mypath + '/spool'):
	os.mkdir(mypath + '/spool')

def handle_interrupt(channel):
	time.sleep(0.003)
	global sensor
	reason = sensor.get_interrupt()
	now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        filename = mypath + '/spool/' + datetime.now().strftime("%Y-%m-%d") + '.lightning.txt'
	outputfile = open(filename , "a" )
	writer = csv.writer(outputfile)
	if reason == 0x01:
		sensor.raise_noise_floor()
		buffer = [now, "Noise level too high"]
		writer.writerow(buffer)
	elif reason == 0x04:
		sensor.set_mask_disturber(True)
		buffer = [now, "Disturber detected"]
		writer.writerow(buffer)
	elif reason == 0x08:
               	GPIO.output(LED, True)
		distance = sensor.get_distance()
		energy = sensor.get_energy()
		buffer = [now, "lightning!" ,  str(distance)  , str(energy)]
		writer.writerow(buffer)
                url = "http://labs.weathernews.jp/hack/lightning/ingest.cgi?id=" + serial_number + "&distance=" + str(distance)  + "&energy=" + str(energy)
                if os.path.exists(mypath + "/proxy.py"):
                        from proxy import proxies
                        resp = requests.get(url,proxies=proxies)
                else:
                        resp = requests.get(url)
	outputfile.close()


IRQ = 17

GPIO.setup(IRQ, GPIO.IN)
GPIO.add_event_detect(IRQ, GPIO.RISING, callback=handle_interrupt)
now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

filename = mypath + '/spool/' + datetime.now().strftime("%Y-%m-%d") + '.lightning.txt'
outputfile = open(filename, "a")
writer = csv.writer(outputfile)
distance = sensor.get_distance()
energy = sensor.get_energy()
buffer = [now, "Waiting for lightning",  str(distance)  , str(energy) ]
writer.writerow(buffer)
outputfile.close()

while True:
	time.sleep(1.0)
	GPIO.output(LED, False)
        if GPIO.input(RST):
                os.system(mypath + "../piset/config/set_config.sh");
                os.system("reboot");
