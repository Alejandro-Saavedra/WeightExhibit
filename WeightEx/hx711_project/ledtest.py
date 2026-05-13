import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PIN = 23
GPIO.setup(PIN, GPIO.OUT, initial=GPIO.LOW)

print("LED should be off for 2s...")
time.sleep(2)

print("led should be on for 5 secs...")
GPIO.output(PIN, GPIO.HIGH)
time.sleep(5)

print("OFF")
GPIO.output(PIN, GPIO.LOW)

GPIO.cleanup()
