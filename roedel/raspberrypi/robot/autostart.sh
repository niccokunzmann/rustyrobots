#!/bin/sh

cd `dirname $0`

log=webserver.py.log

rm $log
touch $log
chown `ls /home | head -1` $log

./webserver.py &>>$log &



