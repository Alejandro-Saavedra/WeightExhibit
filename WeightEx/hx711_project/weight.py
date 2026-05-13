import time
import tkinter as tk
from PIL import Image, ImageTk, ImageColor

import RPi.GPIO as GPIO
from hx711 import HX711 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

 # ---------------- CONFIG ----------------
DOUT_PIN = 6
SCK_PIN = 5

TARE_PIN = 17
MOON_PIN = 12
SUN_PIN = 26
MARS_PIN = 25
JUP_PIN = 21
SPACE_PIN = 22
DISPLAY_MS = 5000

OFFSET = 258980
SCALE_FACTOR = 202.22

READ_SAMPLES = 10
UPDATE_MS = 200

BACKGROUND_IMAGE = "Earth.jpg"
WINDOW_W = 800
WINDOW_H = 480
 # --------------------------------------- 
GPIO.setup(TARE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MOON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SUN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MARS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(JUP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SPACE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

hx = HX711(DOUT_PIN, SCK_PIN)

root = tk.Tk()
root.attributes("-fullscreen", True)
root.overrideredirect(True)
root.config(cursor="none")

root.bind("<Escape>", lambda e: root.destroy())
root.focus_force()

bg_image = Image.open(BACKGROUND_IMAGE).resize((WINDOW_W, WINDOW_H))
bg_photo = ImageTk.PhotoImage(bg_image)

planet_photos = {
    "moon": ImageTk.PhotoImage(Image.open("moon.jpg").resize((WINDOW_W, WINDOW_H))),
    "mars": ImageTk.PhotoImage(Image.open("mars.jpg").resize((WINDOW_W, WINDOW_H))),
    "jupiter": ImageTk.PhotoImage(Image.open("JUPITER.jpg").resize((WINDOW_W, WINDOW_H))),
    "sun": ImageTk.PhotoImage(Image.open("sun.jpg").resize((WINDOW_W, WINDOW_H))),
    "space": ImageTk.PhotoImage(Image.open("space.jpg").resize((WINDOW_W, WINDOW_H))),
}

canvas = tk.Canvas(root, width=WINDOW_W, height=WINDOW_H, highlightthickness=0)
canvas.pack(fill="both", expand=True)

bg_item = canvas.create_image(0, 0, image=bg_photo, anchor="nw")

title = tk.Label(root, text="Weight on Earth", font=("Arial", 26, "bold"), fg="white", bg="black")
value_lbl = tk.Label(root, text="--.- g", font=("Arial", 52, "bold"), fg="white", bg="black")
moon_lbl = tk.Label(root, text="--.- g on the Moon", font=("Arial", 26), fg="white", bg="black")
mars_lbl = tk.Label(root, text="--.- g on Mars", font=("Arial", 26), fg="white", bg="black")
jupiter_lbl = tk.Label(root, text="--.- g on Jupiter", font=("Arial", 26), fg="white", bg="black")
sun_lbl = tk.Label(root, text="--.- g on the Sun", font=("Arial", 26), fg="white", bg="black")
space_lbl = tk.Label(root, text="--.- g in Space", font=("Arial", 26), fg="white", bg="black")
status_lbl = tk.Label(root, text="", font=("Arial", 22), fg="white", bg="black")

canvas.create_window(WINDOW_W // 2, 35, window=title)
canvas.create_window(WINDOW_W // 2, 120, window=value_lbl)
canvas.create_window(WINDOW_W // 2, 430, window=status_lbl)

moon_window_id = canvas.create_window(WINDOW_W // 2, 205, window=moon_lbl)
mars_window_id = canvas.create_window(WINDOW_W // 2, 245, window=mars_lbl)
jupiter_window_id = canvas.create_window(WINDOW_W // 2, 285, window=jupiter_lbl)
sun_window_id = canvas.create_window(WINDOW_W // 2, 325, window=sun_lbl)
space_window_id = canvas.create_window(WINDOW_W // 2, 365, window=space_lbl)

for wid in (moon_window_id, mars_window_id, jupiter_window_id, sun_window_id, space_window_id):
    canvas.itemconfigure(wid, state="hidden")

show_moon = False
show_mars = False
show_jupiter = False
show_sun = False
show_space = False

bg_reset_job = None

def set_background(which=None):
    global bg_reset_job

    if bg_reset_job is not None:
        try:
            root.after_cancel(bg_reset_job)
        except Exception:
            pass
        bg_reset_job = None

    if which is None:
        canvas.itemconfigure(bg_item, image=bg_photo)
    else:
        if which in planet_photos:
            canvas.itemconfigure(bg_item, image=planet_photos[which])
            bg_reset_job = root.after(DISPLAY_MS, lambda: set_background(None))

def read_weight_grams():
    try:
        raw = hx.get_data_mean(READ_SAMPLES)
    except Exception as e:
        status_lbl.config(text=f"Read error: {e}")
        return None, None

    if raw is None:
        return None, None

    grams = (raw - OFFSET) / SCALE_FACTOR
    return grams, raw

def tare():
    global OFFSET
    status_lbl.config(text="Resetting scale...")
    root.update_idletasks()

    try:
        raw = hx.get_data_mean(15)
    except Exception as e:
        status_lbl.config(text=f"Tare failed: {e}")
        return

    if raw is not None:
        OFFSET = raw
        status_lbl.config(text="Tare complete")
    else:
        status_lbl.config(text="Tare failed")

def show_label_temporarily(which):
    global show_moon, show_mars, show_jupiter, show_sun, show_space

    if which in ("moon", "mars", "jupiter", "sun", "space"):
        set_background(which)

    if which == "moon":
        show_moon = True
        canvas.itemconfigure(moon_window_id, state="normal")
        root.after(DISPLAY_MS, lambda: hide_label("moon"))

    elif which == "mars":
        show_mars = True
        canvas.itemconfigure(mars_window_id, state="normal")
        root.after(DISPLAY_MS, lambda: hide_label("mars"))

    elif which == "jupiter":
        show_jupiter = True
        canvas.itemconfigure(jupiter_window_id, state="normal")
        root.after(DISPLAY_MS, lambda: hide_label("jupiter"))

    elif which == "sun":
        show_sun = True
        canvas.itemconfigure(sun_window_id, state="normal")
        root.after(DISPLAY_MS, lambda: hide_label("sun"))

    elif which == "space":
        show_space = True
        canvas.itemconfigure(space_window_id, state="normal")
        root.after(DISPLAY_MS, lambda: hide_label("space"))

def hide_label(which):
    global show_moon, show_mars, show_jupiter, show_sun, show_space

    if which == "moon":
        show_moon = False
        canvas.itemconfigure(moon_window_id, state="hidden")

    elif which == "mars":
        show_mars = False
        canvas.itemconfigure(mars_window_id, state="hidden")

    elif which == "jupiter":
        show_jupiter = False
        canvas.itemconfigure(jupiter_window_id, state="hidden")

    elif which == "sun":
        show_sun = False
        canvas.itemconfigure(sun_window_id, state="hidden")

    elif which == "space":
        show_space = False
        canvas.itemconfigure(space_window_id, state="hidden")

tare_last = 1

def check_tare_button():
    global tare_last
    cur = GPIO.input(TARE_PIN)

    if tare_last == 1 and cur == 0:
        tare()
        root.after(500, check_tare_button)
    else:
        root.after(50, check_tare_button)

    tare_last = cur

moon_last = 1

def check_moon_button():
    global moon_last
    cur = GPIO.input(MOON_PIN)

    if moon_last == 1 and cur == 0:
        show_label_temporarily("moon")
        root.after(250, check_moon_button)
    else:
        root.after(20, check_moon_button)

    moon_last = cur

mars_last = 1

def check_mars_button():
    global mars_last
    cur = GPIO.input(MARS_PIN)

    if mars_last == 1 and cur == 0:
        show_label_temporarily("mars")
        root.after(250, check_mars_button)
    else:
        root.after(20, check_mars_button)

    mars_last = cur

jupiter_last = 1

def check_jupiter_button():
    global jupiter_last
    cur = GPIO.input(JUP_PIN)

    if jupiter_last == 1 and cur == 0:
        show_label_temporarily("jupiter")
        root.after(250, check_jupiter_button)
    else:
        root.after(20, check_jupiter_button)

    jupiter_last = cur

sun_last = 1

def check_sun_button():
    global sun_last
    cur = GPIO.input(SUN_PIN)

    if sun_last == 1 and cur == 0:
        show_label_temporarily("sun")
        root.after(250, check_sun_button)
    else:
        root.after(20, check_sun_button)

    sun_last = cur

space_last = 1

def check_space_button():
    global space_last
    cur = GPIO.input(SPACE_PIN)

    if space_last == 1 and cur == 0:
        show_label_temporarily("space")
        root.after(250, check_space_button)
    else:
        root.after(20, check_space_button)

    space_last = cur

def update():
    try:
        grams, raw = read_weight_grams()

        if grams is None:
            value_lbl.config(text="No data")
        else:
            value_lbl.config(text=f"{int(round(grams))} g")

            if show_moon:
                moon_lbl.config(text=f"{int(grams * 0.165)} g on Moon")
            if show_mars:
                mars_lbl.config(text=f"{int(grams * 0.377)} g on Mars")
            if show_jupiter:
                jupiter_lbl.config(text=f"{int(grams * 2.528)} g on Jupiter")
            if show_sun:
                sun_lbl.config(text=f"{int(grams * 27.9)} g on the Sun")
            if show_space:
                space_lbl.config(text="0 g in Space")

    except Exception as e:
        value_lbl.config(text="Error")
        status_lbl.config(text=f"Update error: {e}")

    root.after(UPDATE_MS, update)

def on_close():
    try:
        GPIO.cleanup()
    except Exception:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

update()
check_tare_button()
check_moon_button()
check_jupiter_button()
check_sun_button()
check_mars_button()
check_space_button()
