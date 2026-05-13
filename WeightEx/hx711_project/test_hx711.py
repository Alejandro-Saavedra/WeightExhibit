from hx711 import HX711
import  RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
hx = HX711(dout_pin=6, pd_sck_pin=5)

print("Printing data (ctrl+c to stop)...")

try:
	while True:
		raw = hx.get_raw_data_mean(5)
		print(raw)
		time.sleep(0.5)

except KeyboardInterrupt:
	pass


GPIO.cleanup()
