from gpiozero import Button
button=Button(4)

button.wait_for_for_press()
print("Button has been pressed")
