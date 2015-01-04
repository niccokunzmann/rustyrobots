import urllib.request
import socket
import re

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_IP)
s.bind(('', 5458))

while 1:
    message = s.recv(1024).decode('UTF-8')
    print(message)
    addresses = re.findall('\d{1,3}(?:\.\d{1,3}){3}(?::\d{1,5})', message)
    if addresses:
        address = addresses[0]
        break

while 1:
    i2 = input('position: ')
    if i2: i = i2
    message = urllib.request.urlopen("http://" + address + "/servo_position/" + i).read()
    print(message.decode('UTF-8'))
