#! /bin/sh
if [ "$1" != "" ]; then
    CONFIG=$1
else
    CONFIG=self_ap
fi

(cd $CONFIG ; tar cfp - .) | (cd / ; tar xf -)


