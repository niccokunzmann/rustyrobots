import webserver
import socket
import urllib.request
import threading
import json
import traceback
import time
import webbrowser
import re

from bottle import run, redirect
from webserver import application as app

s = socket.socket()
try:
    s.bind(("", 80))
except:
    PORT = 8079
else:
    PORT = 80
finally:
    s.close()

listed = set()

def listen_for_robots():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_IP)
    s.bind(('', 5458))
    while 1:
        try:
            message = s.recv(1024)
            if message in listed:
                continue
            listed.add(message)
            message = message.decode('UTF-8')
            addresses = re.findall('\d{1,3}(?:\.\d{1,3}){3}(?::\d{1,5})', message)
            if addresses:
                address = addresses[0]
                information_url = "http://{}/information".format(address)
                with urllib.request.urlopen(information_url) as f:
                    information_json = f.read()
                    charset = f.headers.get_charset()
                    if charset:
                        information_json = information_json.decode(charset)
                    else:
                        information_json = information_json.decode("ASCII")
                information = json.loads(information_json)
                webserver.add_robot(information)
        except:
            traceback.print_exc()

listen_for_robots_thread = threading.Thread(target = listen_for_robots)
listen_for_robots_thread.deamon = True
listen_for_robots_thread.start()

shutdown_lock = threading.Lock()

@app.route('/shutdown')
def shutdown():
    shutdown_lock.release()
    return "shutdown_successful()"

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

@app.route('/addresses')
def get_addresses():
    name, ipv6, ipv4 = socket.gethostbyname_ex(socket.gethostname())
    if not ipv4:
        ip = get_ip_address()
        if not ip:
            ipv4 = ['localhost']
    port = ("" if PORT == 80 else ":{}".format(PORT))
    hostnames = ["http://{}{}".format(host, port) for host in ipv4 + [name]]
    return "add_addresses({})".format(json.dumps(hostnames))

@app.route("/local")
def serve_overview():
    redirect('/static/local.html')

server_thread = threading.Thread(target = run,
                                 args = (app,),
                                 kwargs = dict(host='', port=PORT))
server_thread.deamon = True
server_thread.start()

webbrowser.open("http://localhost:{}/local".format(PORT))

shutdown_lock.acquire()
shutdown_lock.acquire()
time.sleep(1)
