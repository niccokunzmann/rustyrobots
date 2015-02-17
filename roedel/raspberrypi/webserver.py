#!/usr/bin/python3
import threading
from bottle import Bottle, run, request, static_file, response
import time
import socket
import sys
import subprocess
import urllib.parse
import os
import fcntl
import io

from servo_control import *

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


broadcast_thread = threading.Thread(target = broadcast_loop)
broadcast_thread.deamon = True
broadcast_thread.start()

current_subprocess = None

def stop_subprocess():
    global current_subprocess
    if current_subprocess:
        print('writing stop, waiting to close')
        try:
            current_subprocess.stdin.write(b'stop\n')
        except IOError:
            pass
        current_subprocess.wait()
        print('closed')
        current_subprocess = None

def subprocess_code(source_code):
    global current_subprocess, subprocess_output
    stop_subprocess()
    path = os.path.join(os.path.dirname(__file__), 'execute_webcode.py')
    current_subprocess = subprocess.Popen(
        [sys.executable, path, source_code],
        stdin = subprocess.PIPE,
        )
    open('/tmp/subprocess.out', 'w').close()

app = Bottle()

@app.route('/servo_position/<degrees:float>')
def servo_position(degrees):
    subprocess_code('set_servo_position({})'.format(degrees))
    return "Setting servo position to {}°.".format(int(degrees))

@app.route("/execute_python")
def execute_python():
    escaped_python_code = request.query['code']
    source_code = urllib.parse.unquote(escaped_python_code)
    subprocess_code(source_code)
    return 'Executing Python code.'

@app.route("/stop_execution")
def stop_execution():
    stop_subprocess()

@app.route("/output")
def output():
    return static_file('/tmp/subprocess.out', root = '/',
                       mimetype = 'text/plain', charset = 'UTF-8')

@app.route("/exit")
def exit_server():
    stop_subprocess()

set_servo_to_middle()
print("Roedelroboter kann unter {}:{} gesteuert werden.".format(get_ip_address(), PORT))

run(app, host='', port=PORT)
