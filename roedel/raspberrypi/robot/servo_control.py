
try:
    import RPIO
    RPIO_IS_PRESENT = True
except ImportError:
    print('RPIO not installed. Will simulate behavior.')
    RPIO_IS_PRESENT = False

from configuration import SERVO

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

    def set_servo_position(degrees):
        init_servo()
        # compute pulse width
        degrees = degrees % 360
        if degrees > SERVO.ROTATIONAL_RANGE:
            degrees = SERVO.ROTATIONAL_RANGE
        pulse_width = SERVO.PULSE_WIDTH_MIN + \
                      (SERVO.PULSE_WIDTH_MAX - SERVO.PULSE_WIDTH_MIN) * degrees \
                      / SERVO.ROTATIONAL_RANGE

        # pulse the servo
        servo.set_servo(SERVO.PIN, int(pulse_width * 100000) * 10) 

else:
    def set_servo_position(degrees):
        print('set servo position to {}°.'.format(int(degrees)))

def set_servo_to_middle():
    set_servo_position(SERVO.ROTATIONAL_RANGE / 2)

__all__ = ['set_servo_position', 'set_servo_to_middle']
for name in list(globals()):
    if name == name.upper() and name:
        __all__.append(name)
