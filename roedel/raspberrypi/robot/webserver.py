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
import json
import traceback
import io
import re

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
            image = WEBSERVER.ROBOTER_IMAGE_URL,
            add_wifi = url + '/add_wifi',
            remove_wifi = url + '/remove_wifi',
            restart = url + '/restart',
            shutdown = url + '/shutdown',
            update = url + '/update',
            rename = url + '/rename',
            )
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
if os.name == 'nt':
    def get_passwd_output(password):
        return password == 'raspberry'
else:
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

authenticate = auth_basic(check, realm=socket.gethostname())

def callback(*arguments):
    callback_function = request.query.get('callback_function')
    if callback_function:
        response.content_type = 'application/javascript'
        result = "{}({})".format(callback_function,
                                 ", ".join(map(json.dumps, arguments)))
    else:
        response.content_type = 'text/plain'
        result = "\n".join(map(str, arguments))
    return result

def callback_function(function):
    def callback_function(*args, **kw):
        try:
            query = dict(request.query)
            query.pop('callback_function', None)
            query.update(kw)
            result = function(*args, **query)
            if not isinstance(result, str):
                result = result.decode('utf-8')
        except Exception as e:
            file = io.StringIO()
            traceback.print_exc(file = file)
            file.seek(0)
            error = file.read()
            sys.stderr.write(error)
            return callback('error', error)
        else:
            return callback('ok', result)
    return callback_function

wpa_file = "/etc/wpa_supplicant/wpa_supplicant.conf"

@app.route('/add_wifi')
@authenticate
@callback_function
def add_wifi(ssid = "", password = ""):
    assert ssid, "ssid must not be empty"
    assert len(ssid) <= 255, "ssid can have at most 255 characters"
    assert "\n" not in ssid, "ssid must not contain newline"
    result = "\"{}\" added".format(ssid)
    if password:
        assert len(password) <= 255, "password can have at most 255 characters"
        assert "\n" not in password, "password must not contain newline"
        result += " with password"
    assert os.path.isfile(wpa_file), "\"{}\" does not exist".format(wpa_file)
    with open(wpa_file, "a", encoding = "cp1252") as f:
        f.write("\nnetwork={{\n\tssid=\"{}\"".format(ssid))
        if password:
            f.write("\n\tpsk=\"{}\"".format(password))
        f.write("\n}\n")
    return result

@app.route('/remove_wifi')
@authenticate
@callback_function
def remove_wifi(ssid = ""):
    escaped_ssid = re.escape(ssid.encode("cp1252"))
    pattern = b'\nnetwork\s*=\s*{\s*ssid\s*=\s*"' + escaped_ssid + b'"(?:[^\}]|[^\n]\})*\n\}\n?'
    with open(wpa_file, 'rb') as f:
        current_networks = f.read()
    new_networks = re.sub(pattern, b'', current_networks)
    assert isinstance(new_networks, bytes)
    with open(wpa_file, 'wb') as f:
        f.write(new_networks)
    return "removed all \"{}\"".format(ssid)

@app.route('/restart')
@authenticate
@callback_function
def restart():
    return subprocess.check_output(['shutdown', '-r', '0'],
                                   stdin = subprocess.PIPE,
                                   stderr = subprocess.STDOUT)

@app.route('/shutdown')
@authenticate
@callback_function
def shutdown():
    return subprocess.check_output(['shutdown', 'now'],
                                   stdin = subprocess.PIPE,
                                   stderr = subprocess.STDOUT)    

@app.route('/update')
@authenticate
@callback_function
def update():
    github_key = subprocess.check_output(["ssh-keyscan", "-H", "github.com"],
                                   stdin = subprocess.PIPE,
                                   stderr = subprocess.STDOUT ,
                                   cwd = os.path.dirname(__file__))
    known_hosts_file = "/home/pi/.ssh/known_hosts"
    if not os.path.isfile(known_hosts_file) or \
       not any(github_key in line for line in open(known_hosts_file, 'rb')):
        with open(known_hosts_file, "ab") as f:
            f.write(github_key + b'\n')
    command = ["ssh-agent", "bash", "-c", "ssh-add /home/pi/.ssh/id_rsa; git pull origin master"]
    return subprocess.check_output(command,
                                   stdin = subprocess.PIPE,
                                   stderr = subprocess.STDOUT ,
                                   cwd = os.path.dirname(__file__))
    
@app.route('/rename')
@authenticate
@callback_function
def rename(hostname = ""):
    assert all(character.lower() in "-123457890abcdefghijklmnopqrstuvwxyz"
               for character in hostname), "can only contain numbers 0-9 letters a-z and A-Z and the hyphen \"-\""
    assert 1 <= len(hostname), "hostname must not be empty"
    assert len(hostname) <= 255, "hostname can have at most 255 characters"
    hostname_file_path = '/etc/hostname'
    old_hostname = socket.gethostname()
    assert os.path.isfile(hostname_file_path), "\"{}\" does not exist".format(hostname_file_path)
    with open(hostname_file_path, 'w') as f:
        f.write(hostname + "\n")
    return '"{}" => "{}"'.format(old_hostname, hostname)
    

if __name__ == '__main__':
    if not is_servo_server_present():
        start_servo_server()
        
    print("Roedelroboter kann unter {}:{} gesteuert werden.".format(get_ip_address(),
                                                                    WEBSERVER.PORT))

    with open(__file__ + '.pid', 'w') as f:
        f.write(str(os.getpid()))

    run(app, host='', port=WEBSERVER.PORT)
