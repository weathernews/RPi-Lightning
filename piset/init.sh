#! /bin/sh
MYPATH=`dirname $0`
/bin/rm -f $MYPATH/../htdocs/network.json
/bin/rm -f $MYPATH/../htdocs/wlan.txt
/bin/rm -f $MYPATH/../htdocs/location.json
/bin/rm -f $MYPATH/../lightning/*.pyc
/bin/rm -f $MYPATH/../lightning/proxy.py
/bin/rm -rf $MYPATH/../lightning/spool
#$MYPATH/../htdocs/network_save.cgi init
