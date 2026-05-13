import time
import tkinter as tk

import RPi.GPIO as GPIO
from hx711 import HX711

#-----Configuration
DOUT_PIN= 6
SCK_PIN = 5

OFFSET = -184321
SCALE_FACTOR = 425.99

READ_SAMPLES = 10
UPDATE_MS = 200 #GUI UPDATE INTERVAL IN MILLISECONDS
#--------

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

hx = HX711(DOUT_PIN, SCK_PIN)

root = tk.Tk()
root.title(" HX711 Scale")

root.geometry("320x160")

title = tk.Label(root, text=" Weight on Earth ", font=("Arial",18))
title.pack(pady=10)

value_lbl = tk.Label(root, text="--.- g", font=("Arial",32))
value_lbl.pack(pady=5)

moon_lbl = tk.Label(root, text="--.- g on MOON", font=("Arial",16))
moon_lbl.pack(pady=2)

status_lbl = tk.Label(root, text=" ", font=("Arial",10))
status_lbl.pack(pady=5)

def read_weight_grams():
	raw = hx.get_raw_data_mean(READ_SAMPLES)
	if raw is None:
		return None, None
	grams = (raw - OFFSET) / SCALE_FACTOR
	return grams, raw

def update():
	grams, raw = read_weight_grams()
	if grams is None:
		value_lbl.config(text="No Data")
		moon_lbl.config(text="No Data")
		staus_lbl.config(text="Check wiring/pins")
	else:
		value_lbl.config(text=f"{grams:,.1f} g")
		moon_lbl.config(text=f"{grams*.165:,.1f} g on the Moon")
		status_lbl.config(text=f"raw={raw}")
	root.after(UPDATE_MS, update)

def on_close():
	try:
		GPIO.cleanup
	except Exception:
		pass
	root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

update()
root.mainloop()

