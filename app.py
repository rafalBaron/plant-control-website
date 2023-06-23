from flask import Flask, render_template, jsonify, request
import board
import adafruit_bh1750
import datetime
import RPi.GPIO as GPIO
import Adafruit_DHT
import math
import time
import random
import signal
import sys
import spidev
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

dht11_sensor = 4
i2c = board.I2C()
light = 26
pump = 19
spi_ch = 0
PIN_CLK = 11
PIN_DO  = 9
PIN_DI  = 10
PIN_CS  = 8


GPIO.setup(dht11_sensor, GPIO.IN)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(pump, GPIO.OUT)
GPIO.setup(PIN_DI,  GPIO.OUT)
GPIO.setup(PIN_DO,  GPIO.IN)
GPIO.setup(PIN_CLK, GPIO.OUT)
GPIO.setup(PIN_CS,  GPIO.OUT)

def getADC(channel):
	# 1. CS LOW.
        GPIO.output(PIN_CS, True)      # clear last transmission
        GPIO.output(PIN_CS, False)     # bring CS low

	# 2. Start clock
        GPIO.output(PIN_CLK, False)  # start clock low

	# 3. Input MUX address
        for i in [1,1,channel]: # start bit + mux assignment
                 if (i == 1):
                         GPIO.output(PIN_DI, True)
                 else:
                         GPIO.output(PIN_DI, False)

                 GPIO.output(PIN_CLK, True)
                 GPIO.output(PIN_CLK, False)

        # 4. read 8 ADC bits
        ad = 0
        for i in range(8):
                GPIO.output(PIN_CLK, True)
                GPIO.output(PIN_CLK, False)
                ad <<= 1 # shift bit
                if (GPIO.input(PIN_DO)):
                        ad |= 0x1 # set first bit

        # 5. reset
        GPIO.output(PIN_CS, True)

        return ad

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
    
    if sensor.lux <= 6000:
        sensor = round(sensor.lux / 6000 * 100)
    else:
        sensor = 100
    
    light_state = 0
    
    if GPIO.input(light):
        light_state = 1
    else:
        light_state = 0
        
    with open('data.txt', 'r') as file:
        last_water = file.read()
        
    if getADC(1) >= 130:
        soil_hum = round((255 - getADC(1))/125 * 100)
    else:
        soil_hum = 100
        
    if sensor <= 10:
        GPIO.output(light, GPIO.HIGH)
    else:
        GPIO.output(light, GPIO.LOW)
        
    if soil_hum <= 20:
        GPIO.output(pump, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(pump, GPIO.LOW)
    
        with open('data.txt', 'w') as file:
            file.write(str(dataa)+" "+str(hour))
       
    return jsonify(now=now,dataa=dataa,hour=hour,sensor=sensor,temperature=temperature, humidity=humidity,light_state=light_state,soil_hum=soil_hum,last_water=last_water)
    
@app.route('/light_change', methods=['POST'])
def light_change():
    state = request.form['state']
    
    if state == 'on':
        GPIO.output(light, GPIO.HIGH)
    elif state == 'off':
        GPIO.output(light, GPIO.LOW)

    return "OK"
    
@app.route('/podlej', methods=['POST'])
def podlej():
    now = datetime.datetime.now()
    dataa = now.strftime("%d.%m.%Y")
    hour = now.strftime("%H:%M")
    
    GPIO.output(pump, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(pump, GPIO.LOW)
    
    with open('data.txt', 'w') as file:
        file.write(str(dataa)+" "+str(hour))
        
    with open('data.txt', 'r') as file:
            last_water = file.read()
    
    return jsonify(last_water=last_water)

if __name__ == '__main__':
    app.run(debug=True, port=4441, host='0.0.0.0')

