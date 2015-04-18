import os
import json

def local_path(path):
    here = os.path.dirname(__file__)
    return os.path.join(here, path)

CONFIGURATION_FILE = 'configuration.json'

class ConfigurationEntry:
    def __init__(self, dict):
        self.__dict__ = dict

WEBSERVER = ConfigurationEntry(dict(
    PORT = 8080,
    HOST = '',
    BLOCKLY_INDEX_URL = 'https://rawgit.com/niccokunzmann/blockly/master/demos/robots/index.html',
    BLOCKLY_INDEX_PATH = 'demos/robots/index.html',
    BLOCKLY_LOCAL_DIRECTORY = local_path('blockly'),
    REGISTER_SERVER_URL = 'http://rustyrobots.pythonanywhere.com/new_robot',
    ROBOTER_IMAGE_URL = 'https://raw.githubusercontent.com/CoderDojoPotsdam/material/master/roboter/roedelmitraspberrypi/roedelmitraspberrypi.jpg',
    BROADCAST_PORT = 5458,
))

SERVOSERVER = ConfigurationEntry(dict(    
    PORT = 8081,
    HOST = '127.0.0.1',
))

SERVO = ConfigurationEntry(dict(    
    # RPIO uses GPIO pin labeling as default
    PIN = 11,

    # Pulse information for Modelcraft RS2 Servo
    #   http://www.servodatabase.com/servo/modelcraft/rs-2
    PULSE_CYCLE = 0.02, # seconds
    PULSE_WIDTH_MIN = 0.00054, # seconds
    PULSE_WIDTH_MAX = 0.00247, # seconds
    ROTATIONAL_RANGE = 203, # degrees
    # adjusment time according to
    #   http://www.servodatabase.com/servo/modelcraft/rs-2
    # 0.19 sec/60°
    # ROTATIONAL_RANGE / 60 * 0.19 # seconds
    MOVEMENT_SPEED_IN_SECONDS_PER_DEGREES = 0.19 / 60,
    DEFAULT_VELOCITY_MULTIPLIER = 5,
    MINIMUM_VELOCITY_MULTIPLIER = 1,
    MAXIMUM_VELOCITY_MULTIPLIER = 100,
    REACTION_TIME_FOR_NEW_POSITION_IN_SECONDS = 0.1,
))

configuration = dict(
    WEBSERVER = WEBSERVER.__dict__,
    SERVOSERVER = SERVOSERVER.__dict__,
    SERVO = SERVO.__dict__,
)

def load():
    global configuration
    if os.path.isfile(CONFIGURATION_FILE):
        with open(CONFIGURATION_FILE) as f:
            configuration = json.load(f)
            for key, value in configuration.items():
                globals()[key].__dict__ = value

def dump():
    with open(CONFIGURATION_FILE, "w") as f:
        json.dump(configuration, f, sort_keys=True, indent = 4)

load()
