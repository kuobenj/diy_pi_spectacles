import RPi.GPIO
import random
import time
import datetime
import os
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
system_mode = 'photo' # other modes to be supported will be demo and video

#camera object
camera = PiCamera()

def button_callback(button):
    global flash_mode
    global system_mode
    global button2name

    print 'button pressed: ' + repr(button) + ' ' + button2name[button]

    if system_mode == 'button_demo':
        if button == modeBPin:
            system_mode = 'photo'
            flash_mode = False
            # Bring LEDs down
            for led in LEDList:
                if led != statusSPin:
                    RPi.GPIO.setup(led, RPi.GPIO.OUT)
                    RPi.GPIO.output(led, RPi.GPIO.LOW)
        else:
            random_pin = random.randint(0,3)
            RPi.GPIO.output(LEDList[random_pin], not(RPi.GPIO.input(LEDList[random_pin])))

    else: #for now this is just photos
        if button == flashBPin:
            flash_mode = not(flash_mode)
            RPi.GPIO.output(modeSPin, not(RPi.GPIO.input(modeSPin)))

        if button == modeBPin:
            # video mode not implemented yet
            system_mode = 'button_demo'

        if button == functionBPin:
            print 'flash_mode ' + repr(flash_mode)
            if flash_mode:
                RPi.GPIO.output(flashSPin, RPi.GPIO.HIGH)
            camera.capture('/home/pi/diy_pi_spectacles/' + datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S') + '.jpg')
            RPi.GPIO.output(flashSPin, RPi.GPIO.LOW)

        if button == shutdownBPin:
            time.sleep(10)
            if RPi.GPIO.input(shutdownBPin) == RPi.GPIO.LOW:
               print 'SAFE SHUTDOWN COMMENCING'
               # still need to execute shutdown
               # raise KeyboardInterrupt
               RPi.GPIO.cleanup()
               time.sleep(5)
               os.system('sudo shutdown -h now')
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
# camera.resolution = (1920, 1080)
camera.resolution = (2592, 1944)
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