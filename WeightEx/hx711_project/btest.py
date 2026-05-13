import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Same pins from your project
TARE_PIN = 17
MOON_PIN = 12
SUN_PIN = 18

MARS_PIN = 25
JUP_PIN = 21
SPACE_PIN = 22

# Setup with pull-ups
GPIO.setup(TARE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MOON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SUN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MARS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(JUP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SPACE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Press buttons (CTRL+C to quit)\n")

last_states = {
    TARE_PIN: 1,
    MOON_PIN: 1,
    SUN_PIN: 1,
    MARS_PIN: 1,
    JUP_PIN: 1,
    SPACE_PIN: 1,
}

names = {
    TARE_PIN: "TARE",
    MOON_PIN: "MOON",
    SUN_PIN: "SUN",
    MARS_PIN: "MARS",
    JUP_PIN: "JUPITER",
    SPACE_PIN: "SPACE",
}

try:
    while True:
        for pin in last_states:
            current = GPIO.input(pin)

            # detect press (HIGH -> LOW)
            if last_states[pin] == 1 and current == 0:
                print(f"{names[pin]} button pressed")

            last_states[pin] = current

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nExiting...")
    GPIO.cleanup()
