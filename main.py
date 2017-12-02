import RPi.GPIO
import time
import datetime
from picamera import PiCamera

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
button2name = {shutdownBPin :'shutdownBPin', functionBPin : 'functionBPin', modeBPin : 'modeBPin', flashBPin : 'flashBPin'}

flash_mode = False
video_mode = False

#camera object
camera = PiCamera()

def button_callback(button):
    global flash_mode
    global video_mode
    global button2name
    print 'button pressed: ' + repr(button) + ' ' + button2name[button]
    # because for now there's 4 buttons I can cheat a little and map each button to an LED to toggle for a test
    # for i in range(0, len(ButtonList)):
        # if button == ButtonList[i]:
        #     RPi.GPIO.output(LEDList[i], not(RPi.GPIO.input(LEDList[i])))

    if button == flashBPin:
        flash_mode = not(flash_mode)
        RPi.GPIO.output(modeSPin, not(RPi.GPIO.input(modeSPin)))

    if button == modeBPin:
        video_mode = not(video_mode) #this will not be implemented at the moment

    if button == functionBPin:
        print 'flash_mode ' + repr(flash_mode)
        if flash_mode:
            RPi.GPIO.output(flashSPin, RPi.GPIO.HIGH)
        camera.capture(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S') + '.jpg')
        RPi.GPIO.output(flashSPin, RPi.GPIO.LOW)

    if button == shutdownBPin:
        time.sleep(10)
        if RPi.GPIO.input(shutdownBPin) == RPi.GPIO.LOW:
           print 'SAFE SHUTDOWN COMMENCING (JUST A PRINT AT THE MOMENT)'
           # still need to execute shutdown
           # raise KeyboardInterrupt
           RPi.GPIO.cleanup()
           quit()

# Initial Pin Setup:
RPi.GPIO.setmode(RPi.GPIO.BOARD) # Broadcom pin-numbering scheme

# Buttons
for button in ButtonList:
    RPi.GPIO.setup(button, RPi.GPIO.IN, pull_up_down = RPi.GPIO.PUD_UP)
    RPi.GPIO.add_event_detect(button, RPi.GPIO.FALLING, callback=button_callback, bouncetime=500)  # add falling edge detection on a channel

# LED Signals
for led in LEDList:
    RPi.GPIO.setup(led, RPi.GPIO.OUT)
    RPi.GPIO.output(led, RPi.GPIO.HIGH)

# Camera Setup
camera.resolution = (1920, 1080)
camera.rotation = 270
# camera.start_preview()
# Camera warm-up time
time.sleep(2)
# how to capture an image below
# camera.capture('foo.jpg')

# Bring LEDs down
for led in LEDList:
    if led != statusSPin:
        RPi.GPIO.setup(led, RPi.GPIO.OUT)
        RPi.GPIO.output(led, RPi.GPIO.LOW)

# Main loop is only event drivent for this test script
print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        pass
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    RPi.GPIO.cleanup() # cleanup all RPi.GPIO