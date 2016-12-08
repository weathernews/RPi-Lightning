#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import os

RST = 24        # リセット端子
LED = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(RST, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)
pinstat = GPIO.input(RST)
#print " reset pin status %d" % pinstat
if (pinstat == GPIO.HIGH):

    ret = os.system("cmp /home/pi/RPi-Lightning/piset/config/self_ap/etc/network/interfaces  /etc/network/interfaces");
    if (ret == 0):	# already initialized
        GPIO.cleanup()
        exit(0)

    ret = os.system("/home/pi/RPi-Lightning/piset/config/set_config.sh self_ap")
    for i in range(10):
        GPIO.output(LED,GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(LED,GPIO.LOW)
        time.sleep(0.1)
        GPIO.cleanup()
    print " rebooting... "
    os.system("reboot")
