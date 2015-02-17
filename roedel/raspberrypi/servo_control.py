
try:
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
    IS_ON_RASPBERRY_PI = True
except ImportError:
    print('Not running on raspberry pi')
    IS_ON_RASPBERRY_PI = False

SERVO_PIN = 11

HIGH = True
LOW = False

# Pulse information for Modelcraft RS2 Servo
#   http://www.servodatabase.com/servo/modelcraft/rs-2

PULSE_CYCLE = 0.02 # seconds
PULSE_WIDTH_MIN = 0.00054 # seconds
PULSE_WIDTH_MAX = 0.00247 # seconds
ROTATIONAL_RANGE = 203 # degrees
# 0.19 sec/60°
SERVO_ADJUSTMENT_TIME = 1 # ROTATIONAL_RANGE / 60 * 0.19 # seconds


if IS_ON_RASPBERRY_PI:
    def set_servo_position(degrees):
        # compute pulse width
        degrees = degrees % 360
        if degrees > ROTATIONAL_RANGE:
            degrees = ROTATIONAL_RANGE
        pulse_width = PULSE_WIDTH_MIN + (PULSE_WIDTH_MAX - PULSE_WIDTH_MIN) * degrees / ROTATIONAL_RANGE
        # pulse the servo
        servo.set_servo(SERVO_PIN, int(pulse_width * 100000) * 10) 

else:
    def set_servo_position(degrees):
        print('set servo position to {}°.'.format(int(degrees)))

def set_servo_to_middle():
    set_servo_position(ROTATIONAL_RANGE / 2)

__all__ = ['set_servo_position', 'set_servo_to_middle']
