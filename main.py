import RPi.GPIO

# THIS FILE IS BASICALLY A DUPLICATE OF THE TEST

# Pin Definitons:
# BPin implies Button
# SPin implies Output Signal
shutdownBPin    = 11
functionBPin    = 13
modeBPin        = 15
flashBPin       = 37

flashSPin       = 16
recordSPin      = 18
modeSPin        = 22
statusSPin      = 36

ButtonList = [shutdownBPin, functionBPin, modeBPin, flashBPin]
LEDList = [flashSPin, recordSPin, modeSPin, statusSPin]

def button_callback(button):
    print 'button pressed: ' + button
    # because for now there's 4 buttons I can cheat a little and map each button to an LED to toggle for a test
    for i in range(0, len(ButtonList)):
        if button == ButtonList[i]:
            RPi.GPIO.output(LEDList[i], not(RPi.GPIO.input(LEDList[i])))

# Initial Pin Setup:
RPi.GPIO.setmode(RPi.GPIO.BOARD) # Broadcom pin-numbering scheme

# Buttons
for button in ButtonList:
    RPi.GPIO.setup(button, RPi.GPIO.IN, pull_up_down = RPi.GPIO.PUD_UP)
    RPi.GPIO.add_event_detect(button, RPi.GPIO.FALLING, callback=button_callback)  # add falling edge detection on a channel

# LED Signals
for led in LEDList:
    RPi.GPIO.setup(led, RPi.GPIO.OUT)
    RPi.GPIO.output(led, RPi.GPIO.HIGH)

# Main loop is only event drivent for this test script
print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        pass
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    RPi.GPIO.cleanup() # cleanup all RPi.GPIO