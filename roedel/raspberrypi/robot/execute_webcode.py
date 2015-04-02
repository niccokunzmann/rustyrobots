#!/usr/bin/python3
import time
import sys
import threading
from servo_client import *

code = sys.argv[1]

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

