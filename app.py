from flask import Flask, render_template, jsonify, request
import board
import adafruit_bh1750
import datetime
import RPi.GPIO as GPIO
import Adafruit_DHT
import math
import time
import random

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

dht11_sensor = 4
i2c = board.I2C()
light = 21
pump = 13
soil = 6

GPIO.setup(dht11_sensor, GPIO.IN)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(pump, GPIO.OUT)
GPIO.setup(soil, GPIO.IN)

def soil_level(pin):
    if GPIO.input(pin):
        return "SUCHO"
    else:
        return "MOKRO"


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sensor_data_json')
def sensor_data_json():
    now = datetime.datetime.now()
    dataa = now.strftime("%d.%m.%Y")
    hour = now.strftime("%H:%M")
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11,4)
    sensor = adafruit_bh1750.BH1750(i2c)
    sensor = round(sensor.lux / 27306.25 * 100, 2)
    soil_hum_level = soil_level(soil)
    
    return jsonify(now=now,dataa=dataa,hour=hour,sensor=sensor,temperature=temperature, humidity=humidity,soil_hum_level=soil_hum_level)
    
@app.route('/light_change', methods=['POST'])
def light_change():
    state = request.form['state']
    
    if state == 'on':
        GPIO.output(light, GPIO.HIGH)
    elif state == 'off':
        GPIO.output(light, GPIO.LOW)

    return 'OK'
    
@app.route('/watering', methods=['POST'])
def watering():
    now = datetime.datetime.now()
    dataa = now.strftime("%d.%m.%Y")
    hour = now.strftime("%H:%M")
    
    GPIO.output(pump, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(pump, GPIO.LOW)
    
    return jsonify(dataa=dataa, hour=hour)

if __name__ == '__main__':
    app.run(debug=True, port=4441, host='0.0.0.0')

