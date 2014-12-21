import threading
from bottle import Bottle, run
try:
    import RPi.GPIO as GPIO
    IS_ON_RASPBERRY_PI = True
except ImportError:
    print('Not running on raspberry pi')
    IS_ON_RASPBERRY_PI = False
import time

pin = 23

HIGH = False
LOW = True

# Pulse information for Modelcraft RS2 Servo
#   http://www.servodatabase.com/servo/modelcraft/rs-2

PULSE_CYCLE = 0.02 # seconds
PULSE_WIDTH_MIN = 0.00054 # seconds
PULSE_WIDTH_MAX = 0.00247 # seconds

PULSE_WIDTH_MIN = 0.001 # seconds
PULSE_WIDTH_MAX = 0.002 # seconds
ROTATIONAL_RANGE = 203 # degrees


last_servo_pulse = 0

if IS_ON_RASPBERRY_PI:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    def set_servo_position(degrees):
        global last_servo_pulse
        #print("set servo position to {}".format(degrees))
        #now = time.time()
        #if last_servo_pulse + PULSE_CYCLE > now:
        #    time.sleep(last_servo_pulse + PULSE_CYCLE - now)
        #last_servo_pulse = now
        degrees = degrees % 360
        if degrees > ROTATIONAL_RANGE:
            degrees = ROTATIONAL_RANGE
        pulse_width = PULSE_WIDTH_MIN + (PULSE_WIDTH_MAX - PULSE_WIDTH_MIN) * degrees / ROTATIONAL_RANGE
        a = time.time()
        GPIO.output(pin, HIGH)
        time.sleep(pulse_width)
        b = time.time()
        GPIO.output(pin, LOW)
        time.sleep(PULSE_CYCLE)
        print("set servo position to {} {:.6f} {:.6f}".format(degrees, pulse_width, b - a - pulse_width))

else:
    last_servo_position = None
    def set_servo_position(degrees):
        global last_servo_position
        if last_servo_position != degrees:
            print('set servo position to {}°.'.format(int(degrees)))
            last_servo_position = degrees
        time.sleep(0.02)
        

expected_servo_value = 0

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
#set_the_servo_value_thread.start()


app = Bottle()

@app.route('/servo_position/<degrees:float>')
def servo_position(degrees):
    global expected_servo_value
    expected_servo_value = degrees
    if not set_the_servo_value_thread_is_started:
        set_servo_position(degrees)
    return "Setting servo position to {}°.".format(int(degrees))

# run(app, host='', port=8080)

while 1:
    for i in range(100):
        set_servo_position(0)
    for i in range(100):
        set_servo_position(100)
    

