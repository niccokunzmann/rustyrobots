#!/usr/bin/python3
import servo_control
import time
import sys
import threading
import urllib.request

last_degrees = None
lock = threading.Lock()

def _set_servo_position(degrees):
    # direct usage of the servo_control will remove the ability of
    # the server to control the servo
    url = 'http://localhost:{}/servo_position/{}'.format(PORT, degrees)
    r = urllib.request.urlopen(url)
    r.read()
    r.close()

def sleep_until_in_position(degrees):
    global last_degrees
    # adjusment time according to
    #   http://www.servodatabase.com/servo/modelcraft/rs-2
    # 0.19 sec/60°
    if last_degrees is None:
        degree_difference = servo_control.ROTATIONAL_RANGE
    else:
        degree_difference = abs(degrees - last_degrees)
    time_for_rotation = 0.19 * degree_difference / 60
    time.sleep(time_for_rotation)
    last_degrees = degrees

def set_servo_position(degrees = 0):
    with lock:
        _set_servo_position(degrees)
        sleep_until_in_position(degrees)
    

code = sys.argv[1]
PORT = sys.argv[2]

_print = print
def print(*args, **kw):
    _print = globals()['_print']
    if 'file' in kw:
        _print(*args, **kw)
    else:
        with open('/tmp/subprocess.out', 'a', encoding = "UTF-8") as f:
            _print(*args, file = f, **kw)

def run_code():
    exec(code)

thread = threading.Thread(target = run_code)
thread.daemon = True
thread.start()

input()
lock.acquire() # do not run into GPIO code when exiting

