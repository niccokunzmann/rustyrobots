#!/usr/bin/python3

import sys
if len(sys.argv) >= 2 and sys.argv[1] == "-log":
    LOG_FILE = sys.argv[2]
    sys.stdout = sys.stderr = open(LOG_FILE, 'a', encoding = 'UTF-8')
else:
    LOG_FILE = None

import threading
from bottle import Bottle, run, request, static_file, response, redirect
from bottle import auth_basic
import time
import socket
import subprocess
import os
import urllib.request
import urllib.parse
from configuration import SERVOSERVER, WEBSERVER, local_path
from servo_client import *

# broadcast

def get_ip_address(for_local_ip = None):
    if not for_local_ip:
        for_local_ip = '8.8.8.8'
    ip_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # get ip address
    #  from http://stackoverflow.com/a/1267524/1320237
    try:
        ip_sock.connect((for_local_ip, 80))
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
        message = "Der Roedelroboter kann unter {}:{} gesteuert werden.".format(
                                ip_address, WEBSERVER.PORT).encode('UTF-8')
        sock.sendto(message, ('<broadcast>', WEBSERVER.BROADCAST_PORT))
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
        url = 'http://{}:{}'.format(ip, WEBSERVER.PORT)
        robot = dict(
            ip = ip, port = WEBSERVER.PORT, name = socket.gethostname(),
            url = url, echo = url + '/echo',
            image = WEBSERVER.ROBOTER_IMAGE_URL)
        query = WEBSERVER.REGISTER_SERVER_URL + '?' + urllib.parse.urlencode(robot)
        try:
            with urllib.request.urlopen(query) as f:
                print(f.read().decode('utf-8'))
                break
        except urllib.error.URLError as e:
            print('could not register robot at', WEBSERVER.REGISTER_SERVER_URL, '. Reason:', e)
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
        stdout = sys.stdout,
        stderr = sys.stderr,
        )
    open('/tmp/subprocess.out', 'w').close()

app = Bottle()

@app.route('/servo_position/<degrees:float>')
def servo_position(degrees):
    set_servo_position_without_delay(degrees)
    return "Setting servo position to {}°.".format(int(round(degrees)))

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
    query['server'] = "{}:{}".format(get_ip_address(request.remote_addr),
                                     WEBSERVER.PORT)
    if os.path.exists(WEBSERVER.BLOCKLY_LOCAL_DIRECTORY):
        url = os.path.join('/blockly/', WEBSERVER.BLOCKLY_INDEX_PATH)
    else:
        url = WEBSERVER.BLOCKLY_INDEX_URL
    url += '?' + urllib.parse.urlencode(query)
    redirect(url)

@app.route('/blockly/<file:path>')
def serve_blockly(file):
    return static_file(file, root = WEBSERVER.BLOCKLY_LOCAL_DIRECTORY)

@app.route('/log')
def show_log_file():
    if LOG_FILE is None:
        return 'Output is currently not being logged.'
    response.content_type = 'text/plain; charset=UTF8'
    sys.stdout.flush()
    sys.stderr.flush()
    return open(LOG_FILE, 'rb')

# configuration

def get_passwd_output(password):
    if isinstance(password, str):
        password = password.encode('utf8')
    if b'\n' in password or b'\r' in password:
        return False
    p = subprocess.Popen(['sudo', '-u', 'pi', 'passwd', 'pi'],
                         stdin = subprocess.PIPE,
                         stdout = subprocess.PIPE,
                         stderr = subprocess.STDOUT)
    p.stdin.write(password)
    p.stdin.close()
    p.wait()
    return p.stdout.read(1000)

password_mismatch_output = get_passwd_output(b'0\x14\xd88\xce\x9d\xd3\x8b\xb6')

def check(user, password):
    if user != 'pi':
        return False
    return get_passwd_output(password) != password_mismatch_output

@app.route('/configuration')
@auth_basic(check, realm=socket.gethostname())
def configuration():
    return 'success!'

if __name__ == '__main__':
    if not is_servo_server_present():
        start_servo_server()
        
    print("Roedelroboter kann unter {}:{} gesteuert werden.".format(get_ip_address(),
                                                                    WEBSERVER.PORT))

    with open(__file__ + '.pid', 'w') as f:
        f.write(str(os.getpid()))

    run(app, host='', port=WEBSERVER.PORT)
