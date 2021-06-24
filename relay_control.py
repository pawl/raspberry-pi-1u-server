import RPi.GPIO as GPIO
from time import sleep


GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers

relay_pin = int(input('Enter the GPIO pin for the relay to toggle on and off: '))
GPIO.setup(relay_pin, GPIO.OUT)  # GPIO Assign mode
try:
    GPIO.output(relay_pin, GPIO.LOW)  # turn pi off
    sleep(5)
    GPIO.output(relay_pin, GPIO.HIGH)  # turn pi on
    sleep(1)
    print('finished turning relay on and off')
except KeyboardInterrupt:
    GPIO.cleanup()
