import urllib.request

while 1:
    i2 = input('position: ')
    if i2: i = i2
    print(urllib.request.urlopen("http://192.168.0.99:8080/servo_position/" + i).read())
