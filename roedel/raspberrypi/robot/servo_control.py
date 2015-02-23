
try:
    import RPIO
    RPIO_IS_PRESENT = True
except ImportError:
    print('RPIO not installed. Will simulate behavior.')
    RPIO_IS_PRESENT = False

from configuration import SERVO
import threading
import time

current_servo_position = None

if RPIO_IS_PRESENT:
    servo = None
    def init_servo():
        global servo
        if servo is not None:
            return
        import signal

        # PWM traps all signals
        # see https://github.com/metachris/RPIO/issues/15
        # save the signals
        saved_signals = {}
        for s in dir(signal):
            if s.startswith('SIG') and not s.startswith('SIG_'):
                si = getattr(signal, s)
                saved_signals[si] = signal.getsignal(si)
        from RPIO import PWM
        # http://pythonhosted.org/RPIO/pwm_py.html
        servo = PWM.Servo()
        # restore the signals
        for si, h in saved_signals.items():
            if si in (9, 19):
                continue
            signal.signal(si, h)

    servo_lock = threading.Lock()

    def _set_servo_position(degrees):
        global current_servo_position
        init_servo()
        # compute pulse width
        degrees = degrees % 360
        if degrees > SERVO.ROTATIONAL_RANGE:
            degrees = SERVO.ROTATIONAL_RANGE
        pulse_width = SERVO.PULSE_WIDTH_MIN + \
                      (SERVO.PULSE_WIDTH_MAX - SERVO.PULSE_WIDTH_MIN) * degrees \
                      / SERVO.ROTATIONAL_RANGE

        # pulse the servo
        with servo_lock:
            servo.set_servo(SERVO.PIN, int(pulse_width * 100000) * 10)
        current_servo_position = degrees

else:
    def _set_servo_position(degrees):
        global current_servo_position
        print('set servo position to {}°.'.format(int(degrees)))
        current_servo_position = degrees

wanted_servo_position = None

def set_servo_position(degrees):
    global wanted_servo_position
    wanted_servo_position = degrees

def set_servo_to_middle():
    set_servo_position(wanted_servo_position)

servo_velocity_multiplier = SERVO.DEFAULT_VELOCITY_MULTIPLIER

def set_servo_velocity(velocity_multiplier):
    global servo_velocity_multiplier
    velocity_multiplier = float(velocity_multiplier)
    if velocity_multiplier < SERVO.MINIMUM_VELOCITY_MULTIPLIER:
        velocity_multiplier = SERVO.MINIMUM_VELOCITY_MULTIPLIER
    elif velocity_multiplier > SERVO.MAXIMUM_VELOCITY_MULTIPLIER:
        velocity_multiplier = SERVO.MAXIMUM_VELOCITY_MULTIPLIER
    servo_velocity_multiplier = velocity_multiplier

IDLE_SLEEP_TIME = 0.01

def servo_move_loop():
    while 1:
        reaction_time = SERVO.REACTION_TIME_FOR_NEW_POSITION_IN_SECONDS
        if current_servo_position is None or \
           wanted_servo_position  is None:
            time.sleep(reaction_time)
            continue
        if wanted_servo_position < current_servo_position - SERVO.DEGREES_PER_STEP:
            step = -SERVO.DEGREES_PER_STEP
        elif wanted_servo_position > current_servo_position + SERVO.DEGREES_PER_STEP:
            step = SERVO.DEGREES_PER_STEP
        else:
            step = wanted_servo_position - current_servo_position
        if abs(step) > 0.01:
            _set_servo_position(current_servo_position + step)
        sleep_time = step * SERVO.MOVEMENT_SPEED_IN_SECONDS_PER_DEGREES * servo_velocity_multiplier
        if sleep_time < reaction_time:
            time.sleep(reaction_time)
            continue        

servo_move_thread = threading.Thread(target = servo_move_loop)
servo_move_thread.deamon = True
servo_move_thread.start()

__all__ = ['set_servo_position', 'set_servo_to_middle', 'RPIO_IS_PRESENT']
