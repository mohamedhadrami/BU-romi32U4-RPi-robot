from PIL import Image
import os

still = "/home/pi/RPi-Romi-Robot/pi/data/raspistill"

for file in os.listdir(still):
    pic = still+"/"+file
    im = Image.open(pic).convert('RGB')
    width, height = im.size
    left = width/10
    top = 4*height/6
    right = width-width/10
    bottom = height
    im = im.crop((left, top, right, bottom))
    print("done... next")
    im.save(pic)