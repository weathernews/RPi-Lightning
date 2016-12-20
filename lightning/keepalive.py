#!/usr/bin/python
# -*- coding: utf-8 -*-
# 問い合わせ先：株式会社ウェザニューズ
# http://weathernews.jp/c/contact.html

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
from loc import *

def getwlanaddr():
    from subprocess import Popen, PIPE
    proc = Popen(["ifconfig","wlan0"], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    import re
    ptn = re.compile('inet addr:([0-9\.]+)')
    for line in out.split('\n'):
        w = ptn.findall(line)
        if len(w) > 0:
            return w[0]
    return ""

ipaddr = getwlanaddr()
url = "http://labs.weathernews.jp/hack/lightning/alive.cgi?id=" + serial_number + "&lat=" + location_lat + "&lon=" + location_lon + "&ipaddr=" + ipaddr
if os.path.exists(mypath + "/proxy.py"):
    from proxy import proxies
    resp = requests.get(url,proxies=proxies)
else:
    resp = requests.get(url)

