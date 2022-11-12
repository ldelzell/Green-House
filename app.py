import csv
import json
import pandas as pd
from flask import Flask, request
from flask import render_template, send_from_directory

from datetime import datetime

import os
from fhict_cb_01.CustomPymata4 import CustomPymata4



def current_time():
    rightNow = datetime.now()
    time = rightNow.strftime("%I:%M%p")
    time = time.lstrip('0')
    time = time.lower()
    day = rightNow.strftime("%A")

    return "It is " + time + " on " + day + "."

dataList = []

humidity = 0
temperature = None
brightnest_level = 0

max_temperature = float("-inf")
min_temperature = float("inf")

max_humidity = float("-inf")
min_humidity = float("inf")

max_light = float("-inf")
min_light = float("inf")


#clent 2

humidity1 = 0
temperature1 = 0
brightnest_level1 = 0

max_temperature1 = float("-inf")
min_temperature1 = float("inf")

max_humidity1 = float("-inf")
min_humidity1 = float("inf")

max_light1 = float("-inf")
min_light1 = float("inf")
        
def refresh_static():
    global max_temperature, max_humidity, max_light 
    global min_temperature, min_humidity, min_light
    if temperature == None: return

    max_temperature = max(max_temperature, temperature)
    min_temperature = min(min_temperature, temperature)
    max_humidity = max(max_humidity, humidity)
    min_humidity = min(min_humidity, humidity)
    max_light = max(max_light, brightnest_level)
    min_light = min(min_light, brightnest_level)


def refresh_static1():
    global max_temperature1, max_humidity1, max_light1 
    global min_temperature1, min_humidity1, min_light1
    max_temperature1 = max(max_temperature1, temperature1)
    min_temperature1 = min(min_temperature1, temperature1)
    max_humidity1 = max(max_humidity1, humidity1)
    min_humidity1 = min(min_humidity1, humidity1)
    max_light1 = max(max_light1, brightnest_level1)
    min_light1 = min(min_light1, brightnest_level1)



def write_data(value):
    with open("data.csv","a", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(value)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')
@app.route('/data')
def data():
    refresh_static()
    return render_template('data.html',
                            people_names = [],
                            time = current_time(),
                            humidity = humidity,
                            temperature = temperature or "-",
                            brightnest_level = brightnest_level,
                            max_temperature = max_temperature,
                            min_temperature = min_temperature,
                            min_humidity = min_humidity,
                            max_humidity = max_humidity,
                            max_light = max_light,
                            min_light = min_light)


@app.route('/data1')
def data1():

    refresh_static1()
    return render_template('data1.html',
                            people_names = [],
                            time = current_time(),
                            humidity1 = humidity1,
                            temperature1 = temperature1,
                            brightnest_level1 = brightnest_level1,
                            max_temperature1 = max_temperature1,
                            min_temperature1 = min_temperature1,
                            min_humidity1 = min_humidity1,
                            max_humidity1 = max_humidity1,
                            max_light1 = max_light1,
                            min_light1 = min_light1,
                            )

@app.route("/graph")
def graph():
    return render_template("graph.html")


@app.route("/get_data")
def send_data():
    return json.dumps(dataList, separators=(',', ':'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/post_data", methods = ["POST"])
def receive_data():
    global temperature, humidity, brightnest_level, temperature1, humidity1, brightnest_level1, ID, dataList
    json_data = request.get_json()
    hum = float(json_data['humidity'])
    temp = float(json_data['temperature'])
    lig = float(json_data['brightness'])
    dataList.append(json_data)
    if json_data["ID"] == "507486":
        ID = json_data["ID"]
        temperature = temp
        humidity = hum
        brightnest_level = lig
        refresh_static()
    else:
        temperature1 = temp
        humidity1 = hum
        brightnest_level1 = lig
        refresh_static1()

    write_data(json_data)
    return "OK", 200




















