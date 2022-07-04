#!/usr/bin/env python

from picamera import PiCamera
from time import sleep
#from subprocess import call

camera = PiCamera()
#cmd = "raspistill -t 30000 -tl 1000 -o /home/pi/pololu-rpi-slave-arduino-library/pi/images/image.jpg"
#subprocess.call(cmd, shell=True)

camera.start_preview()
sleep(5)
camera.capture('/home/pi/pololu-rpi-slave-arduino-library/pi/images/image.jpg')
camera.stop_preview()