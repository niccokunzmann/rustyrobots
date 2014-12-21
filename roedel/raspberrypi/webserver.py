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

HIGH = True
LOW = False

if IS_ON_RASPBERRY_PI:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    def set_servo_position(degrees):
        expected_value = (degrees % 360) / 360.0
        start = time.time()
        stop = start + 0.003
        GPIO.output(pin, HIGH)
        time.sleep(0.001)
        high = 0.000000000001
        low =  0.000000000001
        last = time.time()
        value = True
        while 1:
            now = time.time()
            if now > stop:
                break
            if value:
                high += now - last
            else:
                low  += now - last
            if high / (high + low) > expected_value:
                if value:
                    GPIO.output(pin, LOW)
                    value = False
            else:
                if not value:
                    GPIO.output(pin, HIGH)
                    value = True
            last = now
        GPIO.output(pin, LOW)
        time.sleep(0.018)
        print("{}% {}% {:.8f} {:.8f}".format(
            int(100 * expected_value), 
            int(high / (high + low) * 100), 
            high, low))
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
set_the_servo_value_thread.start()


app = Bottle()

@app.route('/servo_position/<degrees:float>')
def servo_position(degrees):
    global expected_servo_value
    expected_servo_value = degrees
    if not set_the_servo_value_thread_is_started:
        set_servo_position(degrees)
    return "Setting servo position to {}°.".format(int(degrees))

run(app, host='', port=8080)

