import os
import RPi.GPIO as GPIO
import time
from datetime import datetime


logfile = open("/home/pi/GarageWeb/static/log.txt","a")
logfile.write(datetime.now().strftime("     Program Starting -- %Y/%m/%d -- %H:%M  -- Hello! \n"))
logfile.close()
print(datetime.now().strftime("     Program Starting -- %Y/%m/%d -- %H:%M  -- Hello! \n"))

print " Control + C to exit Program"

GPIO.setmode(GPIO.BOARD)  # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP) # set up pin 18 as an input with a pull-up resistor
time.sleep(1)

TimeDoorOpened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')  #Default Time
DoorOpenTimer = 0  #Default start status turns timer off
DoorOpenTimerMessageSent = 1  #Turn off messages until timer is started

try:
        while 1 >= 0:
            time.sleep(1)
            if DoorOpenTimer == 1:  #Door Open Timer has Started
                currentTimeDate = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
                if (currentTimeDate - TimeDoorOpened).seconds > 900 and DoorOpenTimerMessageSent == 0:
                    print "Your Garage Door has been Open for 15 minutes"
                    DoorOpenTimerMessageSent = 1

            if GPIO.input(18) == GPIO.HIGH and DoorOpenTimer == 1:  #Door is closed
                logfile = open("/home/pi/GarageWeb/static/log.txt", "a")
                logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door Closed \n"))
                logfile.close()
                print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door Closed"))
                DoorOpenTimer = 0
            elif GPIO.input(18) == GPIO.LOW and DoorOpenTimer == 0:
                logfile = open("/home/pi/GarageWeb/static/log.txt", "a")
                logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door Open \n"))
                logfile.close()
                print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door Open"))
                # Start Door Open Timer
                TimeDoorOpened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
                                                   '%Y-%m-%d %H:%M:%S')
                DoorOpenTimer = 1
                DoorOpenTimerMessageSent = 0

except KeyboardInterrupt:
        logfile = open("/home/pi/GarageWeb/static/log.txt","a")
        logfile.write(datetime.now().strftime("     Log Program Shutdown -- %Y/%m/%d -- %H:%M  -- Goodbye! \n"))
        logfile.close()
        print(datetime.now().strftime("     Log Program Shutdown -- %Y/%m/%d -- %H:%M  -- Goodbye! \n"))
        GPIO.cleanup()