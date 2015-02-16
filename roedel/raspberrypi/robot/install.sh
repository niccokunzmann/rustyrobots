#!/bin/sh

sudo apt-get update
sudo apt-get -y install python3-pip
pip-3.2 install RPIO
pip-3.2 install bottle

cd `dirname $0`

./install_autostart.py
