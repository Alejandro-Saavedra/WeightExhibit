import RPi.GPIO as GPIO
from hx711 import HX711
import time 

DOUT_PIN = 6
SCK_PIN = 5
KNOWN_WEIGHT = 200.0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

hx= HX711(DOUT_PIN,SCK_PIN)

print("\n---HX711 Calibration (200g)---")
print("1) Remove all weight from the scale")
print("Press Enter to tare...")

#Tare
offset = hx.get_raw_data_mean(15)
print(f"Offset set to : {offset}")

print("\n2) Place the 200g weight on the scale.")
input("Press Enter when stable...")

raw = hx.get_raw_data_mean(15)
print(f"Raw reading with weight: {raw}")

#Calculating scale factor
difference = raw - offset
if difference == 0:
	print("Error: no change detected.")
	GPIO.cleanup()
	raise SystemExit(1)

scale_factor = difference / KNOWN_WEIGHT


print("\n CALIBRATION IS COMPLETE!!!!!!!")
print(f"SCALE FACTOR = {scale_factor}")
print("Now showing live readings im grams (Ctrl+C to stop):\n")

try:
	while True:
		raw_now = hx.get_raw_data_mean(10)
		weight = (raw_now - offset) / scale_factor
		print(f"{weight:.2f} g")
		time.sleep(0.5)
except KeyboardInterrupt:
	pass

GPIO.cleanup()

