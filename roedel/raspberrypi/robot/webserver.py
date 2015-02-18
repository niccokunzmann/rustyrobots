#!/usr/bin/python3
import threading
from bottle import Bottle, run, request, static_file, response, redirect
import time
import socket
import sys
import subprocess
import urllib.parse
import os
import fcntl
import io
import urllib.request
import urllib.parse

from servo_control import *

PORT = 8080
INDEX_URL = 'https://rawgit.com/niccokunzmann/blockly/master/demos/robots/index.html'
REGISTER_SERVER_URL = 'http://rustyrobots.pythonanywhere.com/new_robot'
ROBOTER_IMAGE_URL = 'https://raw.githubusercontent.com/niccokunzmann/rustyrobots/master/roedel/versions/roedel%20v0.2.2%20arduino.jpg'
BROADCAST_PORT = 5458

# broadcast

def get_ip_address():
    ip_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # get ip address
    #  from http://stackoverflow.com/a/1267524/1320237
    try:
        ip_sock.connect(('8.8.8.8', 80))
    except socket.error:
        return ''
    ip_address = ip_sock.getsockname()[0]
    ip_sock.close()
    return ip_address


def broadcast_loop():
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  
   sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
   while 1:
        ip_address = get_ip_address()
        message = "Der Roedelroboter kann unter {}:{} gesteuert werden.".format(ip_address, PORT).encode('UTF-8')
        sock.sendto(message, ('<broadcast>', BROADCAST_PORT))
        time.sleep(1)


broadcast_thread = threading.Thread(target = broadcast_loop)
broadcast_thread.deamon = True
broadcast_thread.start()

current_subprocess = None

def register_server():
    while 1:
        ip = get_ip_address()
        if not ip:
            time.sleep(5)
            continue
        url = 'http://{}:{}'.format(ip, PORT)
        robot = dict(
            ip = ip, port = PORT, name = socket.gethostname(),
            url = url, echo = url + '/echo',
            image = ROBOTER_IMAGE_URL)
        query = REGISTER_SERVER_URL + '?' + urllib.parse.urlencode(robot)
        try:
            with urllib.request.urlopen(query) as f:
                print(f.read().decode('utf-8'))
                break
        except urllib.error.URLError as e:
            print('could not register robot at', REGISTER_SERVER_URL, '. Reason:', e)
            time.sleep(5)
            
register_server_thread = threading.Thread(target = register_server)
register_server_thread.deamon = True
register_server_thread.start()

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
    subprocess_code('_set_servo_position({})'.format(degrees))
    return "Setting servo position to {}°.".format(int(degrees))

@app.route("/execute_python")
def execute_python():
    escaped_python_code = request.query['code']
    source_code = escaped_python_code.encode('raw_unicode_escape').decode('utf-8')
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

@app.route("/echo")
def echo():
    return request.query['content']

@app.route('/')
def root():
    query = dict(request.query)
    query['server'] = "{}:{}".format(get_ip_address(), PORT)
    url = INDEX_URL
    url += '?' + urllib.parse.urlencode(query)
    redirect(url)

@app.route('/log')
def show_log_file():
    return static_file('webserver.py.log', root = '.',
                       mimetype = 'text/plain', charset = 'UTF-8')

set_servo_to_middle()
print("Roedelroboter kann unter {}:{} gesteuert werden.".format(get_ip_address(), PORT))

with open(__file__ + '.pid', 'w') as f:
    f.write(str(os.getpid()))

run(app, host='', port=PORT)
