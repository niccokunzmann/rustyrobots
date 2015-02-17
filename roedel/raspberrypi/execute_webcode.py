#!/usr/bin/python3
from servo_control import set_servo_position as _set_servo_position
import time
import sys
import threading

_print = print
real_stdout = sys.stdout
sys.stdout = sys.stderr

lock = threading.Lock()

def set_servo_position(degrees):
    with lock:
        _set_servo_position(degrees)

code = sys.argv[1]

def run_code():
    def print(*args, **kw):
        if 'file' in kw:
            _print(*args, **kw)
        else:
            _print(*args, file = real_stdout, **kw)
    exec(code)

thread = threading.Thread(target = run_code)
thread.daemon = True
thread.start()

print(code)
input('Press ENTER to quit:')
lock.acquire() # do not run into GPIO code when exiting
exit(0)
