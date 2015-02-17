#!/usr/bin/python3
import threading
from bottle import Bottle, run, request
try:
    from RPIO import PWM
    # http://pythonhosted.org/RPIO/pwm_py.html
    servo = PWM.Servo()
    IS_ON_RASPBERRY_PI = True
except ImportError:
    print('Not running on raspberry pi')
    IS_ON_RASPBERRY_PI = False
import time
import socket
import sys
import subprocess
import urllib.parse

PORT = 8080

# broadcast

def get_ip_address():
    ip_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # get ip address
    #  from http://stackoverflow.com/a/1267524/1320237
    ip_sock.connect(('8.8.8.8', 80))
    ip_address = ip_sock.getsockname()[0]
    ip_sock.close()
    return ip_address


def broadcast_loop():
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  
   sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
   while 1:
        ip_address = get_ip_address()
        message = "Der Roedelroboter kann unter {}:{} gesteuert werden.".format(ip_address, PORT).encode('UTF-8')
        sock.sendto(message, ('<broadcast>', 5458))
        time.sleep(1)

pin = 11

HIGH = True
LOW = False

# Pulse information for Modelcraft RS2 Servo
#   http://www.servodatabase.com/servo/modelcraft/rs-2

PULSE_CYCLE = 0.02 # seconds
PULSE_WIDTH_MIN = 0.00054 # seconds
PULSE_WIDTH_MAX = 0.00247 # seconds
ROTATIONAL_RANGE = 203 # degrees
# 0.19 sec/60°
SERVO_ADJUSTMENT_TIME = 1 # ROTATIONAL_RANGE / 60 * 0.19 # seconds


if IS_ON_RASPBERRY_PI:
    def set_servo_position(degrees):
        # compute pulse width
        degrees = degrees % 360
        if degrees > ROTATIONAL_RANGE:
            degrees = ROTATIONAL_RANGE
        pulse_width = PULSE_WIDTH_MIN + (PULSE_WIDTH_MAX - PULSE_WIDTH_MIN) * degrees / ROTATIONAL_RANGE
        # pulse the servo
        servo.set_servo(pin, int(pulse_width * 100000) * 10) 

else:
    def set_servo_position(degrees):
        print('set servo position to {}°.'.format(int(degrees)))

broadcast_thread = threading.Thread(target = broadcast_loop)
broadcast_thread.deamon = True
broadcast_thread.start()

current_subprocess = None



app = Bottle()

@app.route('/servo_position/<degrees:float>')
def servo_position(degrees):
    set_servo_position(degrees)
    return "Setting servo position to {}°.".format(int(degrees))

@app.route("/execute_python")
def execute_python():
    escaped_python_code = request.query['code']
    source_code = urllib.parse.unquote(escaped_python_code)
    print(source_code)

set_servo_position(ROTATIONAL_RANGE / 2)
print("Roedelroboter kann unter {}:{} gesteuert werden.".format(get_ip_address(), PORT))

run(app, host='', port=PORT)
