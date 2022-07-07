#!/usr/bin/env python

from picamera import PiCamera
from time import sleep
from PIL import Image
#from subprocess import call

camera = PiCamera()
#take pictures every second for 10 seconds and store to known location
#cmd = "raspistill -t 10000 -tl 1000 -o /home/pi/RPi-Romi-Robot/pi/data/raspistill/image%04d.jpg"
#subprocess.call(cmd, shell=True)

camera.resolution = (1600, 1200)
#camera.crop = (0.25, 0.25, 0.5, 0.5)
camera.start_preview()
sleep(5)
camera.capture('/home/pi/RPi-Romi-Robot/pi/data/image.jpg')

im = Image.open('/home/pi/RPi-Romi-Robot/pi/data/image.jpg').convert('RGB')
width, height = im.size
left = width/10
top = height/2
right = width-width/10
bottom = height
im = im.crop((left, top, right, bottom))
im.save('/home/pi/RPi-Romi-Robot/pi/data/image.jpg')

camera.stop_preview()