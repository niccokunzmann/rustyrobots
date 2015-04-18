#!/usr/bin/python3
import urllib.request
from configuration import SERVO, SERVOSERVER
import threading
import socket
import sys
import os
import subprocess
import time
import re

last_degrees = None

def make_request(path):
    url = 'http://{}:{}/{}'.format(SERVOSERVER.HOST, SERVOSERVER.PORT,
                                    path)
    with urllib.request.urlopen(url) as r:
        s = r.read()
    if isinstance(s, bytes):
        s = s.decode('UTF-8')
    return s    

def set_servo_position_without_delay(degrees):
    # direct usage of the servo_control will remove the ability of
    # the server to control the servo
    s = make_request('servo_position/{}'.format(degrees))
    time_to_arrive = re.findall("(\\d+)\s*milliseconds", s)
    if time_to_arrive:
        return int(time_to_arrive[0]) / 1000.
    return SERVO.ROTATIONAL_RANGE * SERVO.MOVEMENT_SPEED_IN_SECONDS_PER_DEGREES

def set_servo_position(degrees = 0):
    time_to_arrive = set_servo_position_without_delay(degrees)
    time.sleep(time_to_arrive)
    return 0

def set_servo_velocity(multiplier = SERVO.DEFAULT_VELOCITY_MULTIPLIER):
    s = make_request('servo_velocity/{}'.format(multiplier))
    multiplier_ = re.findall("'([^']*?)'", s)
    if multiplier_:
        return int(multiplier_[0])
    return multiplier

def is_servo_server_present():
    s = socket.socket()
    try:
        s.connect((SERVOSERVER.HOST, SERVOSERVER.PORT))
    except:
        return False
    else:
        return True
    finally:
        s.close()

def start_servo_server():
    server_path = os.path.join(os.path.dirname(__file__), 'servo_server.py')
    return subprocess.Popen([sys.executable, server_path])
    
__all__ = ['set_servo_position_without_delay', 'set_servo_velocity', 
           'set_servo_position', 'is_servo_server_present', 'start_servo_server']
