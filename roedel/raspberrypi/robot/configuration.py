
class WEBSERVER:

    PORT = 8080
    HOST = ''
    INDEX_URL = 'https://rawgit.com/niccokunzmann/blockly/master/demos/robots/index.html'
    REGISTER_SERVER_URL = 'http://rustyrobots.pythonanywhere.com/new_robot'
    ROBOTER_IMAGE_URL = 'https://raw.githubusercontent.com/niccokunzmann/rustyrobots/master/roedel/versions/roedel%20v0.2.2%20arduino.jpg'
    BROADCAST_PORT = 5458

class SERVOSERVER:
    
    PORT = 8081
    HOST = 'localhost'

class SERVO:

    # RPIO uses GPIO pin labeling as default
    PIN = 11

    # Pulse information for Modelcraft RS2 Servo
    #   http://www.servodatabase.com/servo/modelcraft/rs-2
    PULSE_CYCLE = 0.02 # seconds
    PULSE_WIDTH_MIN = 0.00054 # seconds
    PULSE_WIDTH_MAX = 0.00247 # seconds
    ROTATIONAL_RANGE = 203 # degrees
    # adjusment time according to
    #   http://www.servodatabase.com/servo/modelcraft/rs-2
    # 0.19 sec/60°
    # ROTATIONAL_RANGE / 60 * 0.19 # seconds
    MOVEMENT_SPEED_IN_SECONDS_PER_DEGREES = 0.19 / 60
