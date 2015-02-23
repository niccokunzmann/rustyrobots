#!/usr/bin/python3
from servo_control import *
from configuration import SERVOSERVER

from bottle import Bottle, run
import threading

app = Bottle()

@app.route('/servo_position/<degrees:float>')
def servo_position(degrees):
    set_servo_position(degrees)
    return "Setting servo position to {}°.".format(int(round(degrees)))

@app.route('/servo_velocity/<multiplier:float>')
def servo_velocity(multiplier):
    multiplier = set_servo_velocity(multiplier)
    return "Setting servo velocity to {}.".format(int(round(multiplier)))

set_servo_to_middle()

if __name__ == '__main__':
    server_thread = threading.Thread(target = run, 
                                         args = (app,),
                                         kwargs = dict(host = SERVOSERVER.HOST,
                                                       port = SERVOSERVER.PORT))
    server_thread.deamon = True
    server_thread.start()
    servo_move_loop()
