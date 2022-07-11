from a_star import AStar
a_star = AStar()

import subprocess
import hardwareside
from time import sleep
d = 1

def action(lbl):
    #call(['/home/pi/RPi-Romi-Robot/pi/hardwareside.py'])
    if lbl =='left':
        a_star.motors(0,50)
        sleep(d)
        a_star.motors(0,0)
    elif lbl =='right':
        a_star.motors(50,0)
        sleep(d)
        a_star.motors(0,0)
    elif lbl =='straight':
        a_star.motors(50,50)
        sleep(d)
        a_star.motors(0,0)
    elif lbl =='bag':
        a_star.motors(0,0)
    return ""

while True:
    subprocess.call(['/home/pi/RPi-Romi-Robot/pi/camera.py'])
    #call(['/home/pi/RPi-Romi-Robot/pi/hardwareside.py']) #use chmod 755 <path> for permission to file
    cmd = "python3 /home/pi/RPi-Romi-Robot/pi/hardwareside.py"
    subprocess.call(cmd, shell=True)
    #import hardwareside
    lbl = detect.lbl_max
    action(lbl)
    print("Lhbvasjdab:____"+lbl)
    
a_star.motors(0,0)

