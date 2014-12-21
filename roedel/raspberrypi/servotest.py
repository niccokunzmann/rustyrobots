import RPi.GPIO as GPIO
import time

pin = 23
refresh_period = 0.02

GPIO.setmode(GPIO.BOARD)

GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, True)

print("Steuere Servo auf Pin {}".format(pin))

while True:
    print("links")
    t = time.time() + 0.5
    while time.time() < t:
        GPIO.output(pin, True)
        time.sleep(0.001)
        GPIO.output(pin, False)
        time.sleep(0.019)

    print("rechts")
    t = time.time() + 0.5
    while time.time() < t:
        GPIO.output(pin, True)
        time.sleep(0.002)
        GPIO.output(pin, False)
        time.sleep(0.018)
    
#    for i in range(1, 100):
#        GPIO.output(pin, False)
#        time.sleep(0.001)
#        GPIO.output(pin, True)
#        time.sleep(refresh_period)

#    for i in range(1, 100):
#        GPIO.output(pin, False)
#        time.sleep(0.0015)
#        GPIO.output(pin, True)
#        time.sleep(refresh_period)

#    for i in range(1, 100):
#        GPIO.output(pin, False)
#        time.sleep(0.002)
#        GPIO.output(pin, True)
#        time.sleep(refresh_period)
