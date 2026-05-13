from gpiozero import Button, LED
import time
button=Button(4)
led=LED(17)
while True:
	button.wait_for_press()
	print("It worked")
	led.toggle()
	time.sleep(0.5)
