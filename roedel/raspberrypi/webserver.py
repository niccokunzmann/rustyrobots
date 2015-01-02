import threading
from bottle import Bottle, run
try:
    import RPi.GPIO as GPIO
    IS_ON_RASPBERRY_PI = True
except ImportError:
    print('Not running on raspberry pi')
    IS_ON_RASPBERRY_PI = False
import time
import socket
import sys

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

pin = 23

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

last_servo_pulse = 0
last_servo_position = None
last_servo_position_time = 0


if IS_ON_RASPBERRY_PI:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    def set_servo_position(degrees):
        global last_servo_pulse, last_servo_position, last_servo_position_time
        now = time.time()
        # wait for the cycle
        if last_servo_pulse + PULSE_CYCLE > now:
            time.sleep(last_servo_pulse + PULSE_CYCLE - now)
        last_servo_pulse = time.time()
        # do not pulse the servo if the position is reached to avoid jitter
        if last_servo_position == degrees:
            if last_servo_position_time + SERVO_ADJUSTMENT_TIME < now:
                return
        else:
            last_servo_position_time = now
            last_servo_position = degrees
        # compute pulse width
        degrees = degrees % 360
        if degrees > ROTATIONAL_RANGE:
            degrees = ROTATIONAL_RANGE
        pulse_width = PULSE_WIDTH_MIN + (PULSE_WIDTH_MAX - PULSE_WIDTH_MIN) * degrees / ROTATIONAL_RANGE
        # pulse the servo
        GPIO.output(pin, HIGH)
        time.sleep(pulse_width)
        GPIO.output(pin, LOW)

else:
    last_servo_position = None
    def set_servo_position(degrees):
        global last_servo_position
        if last_servo_position != degrees:
            print('set servo position to {}°.'.format(int(degrees)))
            last_servo_position = degrees
        time.sleep(0.02)
        

expected_servo_value = ROTATIONAL_RANGE / 2

def set_the_servo_value_loop():
    global set_the_servo_value_thread_is_started
    set_the_servo_value_thread_is_started = True
    try:
        while 1:
            set_servo_position(expected_servo_value)
    finally:
        set_the_servo_value_thread_is_started = False

set_the_servo_value_thread_is_started = False
set_the_servo_value_thread = threading.Thread(target = set_the_servo_value_loop)
set_the_servo_value_thread.deamon = True
set_the_servo_value_thread.start()


broadcast_thread = threading.Thread(target = broadcast_loop)
broadcast_thread.deamon = True
broadcast_thread.start()


app = Bottle()

@app.route('/servo_position/<degrees:float>')
def servo_position(degrees):
    global expected_servo_value
    expected_servo_value = degrees
    if not set_the_servo_value_thread_is_started:
        set_servo_position(degrees)
    return "Setting servo position to {}°.".format(int(degrees))

print("Roedelroboter kann unter {}:{} gesteuert werden.".format(get_ip_address(), PORT))

run(app, host='', port=PORT)
