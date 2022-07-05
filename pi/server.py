#!/usr/bin/env python3

# Copyright Pololu Corporation.  For more information, see https://www.pololu.com/
from flask import Flask
from flask import render_template
from flask import redirect
from flask import send_file
from subprocess import call
app = Flask(__name__)
app.debug = True

from a_star import AStar
a_star = AStar()

import hardwareside
import os
import json

led0_state = False
led1_state = False
led2_state = False

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/status.json")
def status():
    buttons = a_star.read_buttons()
    analog = a_star.read_analog()
    battery_millivolts = a_star.read_battery_millivolts()
    encoders = a_star.read_encoders()
    data = {
        "buttons": buttons,
        "battery_millivolts": battery_millivolts,
        "analog": analog,
        "encoders": encoders
    }
    return json.dumps(data)

@app.route("/motors/<left>,<right>")
def motors(left, right):
    a_star.motors(int(left), int(right))
    return ""

@app.route("/classify/<classnote>")
def classify(classnote):
    call(['/home/pi/pololu-rpi-slave-arduino-library/pi/camera.py'])
    #call(['/home/pi/pololu-rpi-slave-arduino-library/pi/hardwareside.py']) #use chmod 755 <path> for permission to file
    if hardwareside.classification_label == 'left':
        a_star.motors(-100,100)
        #sleep(1000)
        a_star.motors(0,0)
    elif hardwareside.classification_label =='right':
        a_star.motors(100,-100)
        #sleep(1000)
        a_star.motors(0,0)
    elif hardwareside.classification_label =='straight':
        a_star.motors(100,100)
        #sleep(1000)
        a_star.motors(0,0)
    elif hardwareside.classification_label =='bag':
        a_star.servo(1500)
        #sleep(1000)
        a_star.servo(2000)
    else:
        a_star.play_notes(classnote)
    return ""

@app.route("/servo/<setServo>")
def servo(setServo):
    a_star.servo(int(setServo))
    return ""

@app.route("/pic")
def pic():
    #call(['/home/pi/pololu-rpi-slave-arduino-library/pi/camera.py'])
    picture = "/home/pi/Desktop/data/image.jpeg"
    hello()
    return send_file(picture)

@app.route("/logo")
def logo():
    logo = "images/Bshield_rgb.jpg"
    return send_file(logo)

@app.route("/leds/<int:led0>,<int:led1>,<int:led2>")
def leds(led0, led1, led2):
    a_star.leds(led0, led1, led2)
    global led0_state
    global led1_state
    global led2_state
    led0_state = led0
    led1_state = led1
    led2_state = led2
    return ""

@app.route("/heartbeat/<int:state>")
def hearbeat(state):
    if state == 0:
      a_star.leds(led0_state, led1_state, led2_state)
    else:
        a_star.leds(not led0_state, not led1_state, not led2_state)
    return ""

@app.route("/play_notes/<notes>")
def play_notes(notes):
    a_star.play_notes(notes)
    return ""

@app.route("/halt")
def halt():
    call(["bash", "-c", "(sleep 2; sudo halt)&"])
    return redirect("/shutting-down")

@app.route("/shutting-down")
def shutting_down():
    return "Shutting down in 2 seconds! You can remove power when the green LED stops flashing."

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port="7000")
