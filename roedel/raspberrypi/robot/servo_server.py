#!/usr/bin/python3
from servo_control import *
from configuration import SERVOSERVER

from bottle import Bottle, run

app = Bottle()

@app.route('/servo_position/<degrees:float>')
def servo_position(degrees):
    set_servo_position(degrees)
    return "Setting servo position to {}°.".format(int(round(degrees)))

set_servo_to_middle()

if __name__ == '__main__':
    run(app, host=SERVOSERVER.HOST, port=SERVOSERVER.PORT)
