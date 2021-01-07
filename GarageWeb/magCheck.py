import RPi.GPIO as GPIO
import sys
channel = 18
GPIO.setmode(GPIO.BOARD)
# Setup your channel
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# To test the value of a pin use the .input method
channel_is_on = GPIO.input(channel)  # Returns 0 if OFF or 1 if ON

if GPIO.input(channel) == GPIO.LOW:
    print("Garage is Open")
else:
    print("Closed!")
GPIO.cleanup()