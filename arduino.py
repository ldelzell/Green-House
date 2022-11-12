from datetime import datetime
import time
from fhict_cb_01.CustomPymata4 import CustomPymata4
from requests import request
import requests


DHTPIN  = 12 
LDRPIN = 2

ID="507486"

def Measure(data):
    global humidity, temperature
    if (data[3] == 0):
        humidity = data[4]
        temperature = data[5]

def LDRChanged(data):
    global brightnest_level
    brightnest_level = data[2]

board = CustomPymata4(com_port = "COM3")
board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05, callback=Measure)
board.set_pin_mode_analog_input(LDRPIN, callback = LDRChanged, differential = 10)

while True:
    time.sleep(5)
    time_stamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    data = {'ID':ID, 'time_stamp': time_stamp, 'humidity':humidity, 'temperature':temperature, 'brightness':brightnest_level}
    response = requests.post("http://localhost:5000/post_data", json= data)
    print(response)

