import RPi.GPIO as GPIO
import time

PIN = 22 # your Mars pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        print(GPIO.input(PIN))
        time.sleep(0.2)
except KeyboardInterrupt:
	GPIO.cleanup()

