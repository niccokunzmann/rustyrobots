#!/usr/bin/python3
import urllib.request
from configuration import SERVO, SERVOSERVER
import threading
import socket
import sys
import os
import subprocess

last_degrees = None

def set_servo_position_without_delay(degrees):
    # direct usage of the servo_control will remove the ability of
    # the server to control the servo
    url = 'http://{}:{}/servo_position/{}'.format(SERVOSERVER.HOST, SERVOSERVER.PORT,
                                                  degrees)
    r = urllib.request.urlopen(url)
    r.read()
    r.close()

def sleep_until_in_position(degrees):
    global last_degrees
    if last_degrees is None:
        degree_difference = SERVO.ROTATIONAL_RANGE
    else:
        degree_difference = abs(degrees - last_degrees)
    time_for_rotation = degree_difference * SERVO.MOVEMENT_SPEED_IN_SECONDS_PER_DEGREES
    time.sleep(time_for_rotation)
    last_degrees = degrees

def set_servo_position(degrees = 0):
    set_servo_position_without_delay(degrees)
    sleep_until_in_position(degrees)

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
    
__all__ = ['set_servo_position_without_delay', 'sleep_until_in_position',
           'set_servo_position', 'is_servo_server_present', 'start_servo_server']
