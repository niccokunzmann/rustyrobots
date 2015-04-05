#!/bin/sh

cd `dirname $0`

log=webserver.py.log

rm $log
touch $log
chown `ls /home | head -1` $log

# http://serverfault.com/questions/132970/can-i-automatically-add-a-new-host-to-known-hosts
ssh-keyscan -H github.com >> ~/.ssh/known_hosts
ssh-keyscan -H github.com >> /root/.ssh/known_hosts

./webserver.py -log $log &



