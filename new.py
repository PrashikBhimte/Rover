import RPi.GPIO as GPIO
import datetime
from flask import Flask, render_template, request, jsonify
import os, json
import Adafruit_DHT

dht_sensor = Adafruit_DHT.DHT11

rover = Flask(__name__)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

IR1_pin = 7
IR2_pin = 11
DHT_pin = 13
mositure_pin = 15
EnA = 19
EnB = 21
A1 = 23
A2 = 29
B1 = 31
B2 = 33

IR1_value = GPIO.LOW
IR2_value = GPIO.LOW
mositure_value = GPIO.LOW

GPIO.setup(IR1_pin, GPIO.IN)
GPIO.setup(IR2_pin, GPIO.IN)
GPIO.setup(DHT_pin, GPIO.IN)
GPIO.setup(mositure_pin, GPIO.IN)

GPIO.setup(EnA, GPIO.OUT)
GPIO.setup(EnB, GPIO.OUT)
GPIO.setup(A1, GPIO.OUT)
GPIO.setup(A2, GPIO.OUT)
GPIO.setup(B1, GPIO.OUT)
GPIO.setup(B2, GPIO.OUT)

GPIO.output(EnA, GPIO.HIGH)
GPIO.output(EnB, GPIO.HIGH)


@rover.route('/', methods=['GET', 'POST'])
def index():
    json_url = os.path.join('data', 'data.json')
    IR1_value = GPIO.input(IR1_pin)
    IR2_value = GPIO.input(IR2_pin)
    mositure_value = GPIO.input(mositure_pin)

    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, DHT_pin)

    now = datetime.datetime.now()
    timestr = now.strftime("%Y-%m-%d %H:%M")

    templateData = {
        'IR1_data': IR1_value,
        'IR2_data': IR2_value,
        'humidity': humidity,
        'temperature': temperature,
        'mositure': mositure_value,
        'time': timestr
    }

    with open(json_url, 'r+') as file:
        data = json.load(file)
        data["Data"].clear()
        data["Data"] = templateData
        file.seek(0)
        json.dump(data, file)

    if request.method == 'GET':
        data_json = json.load(open(json_url))
        data = data_json["Data"]


    if request.method == 'POST':
        MDdata = request.get_data()

        print(MDdata)

        if MDdata == b'"f"':
            print("forward")
            GPIO.output(A1, GPIO.HIGH)
            GPIO.output(A2, GPIO.LOW)
            GPIO.output(B1, GPIO.HIGH)
            GPIO.output(B2, GPIO.LOW)

        if MDdata == b'"b"':
            print("backward")
            GPIO.output(A1, GPIO.LOW)
            GPIO.output(A2, GPIO.HIGH)
            GPIO.output(B1, GPIO.LOW)
            GPIO.output(B2, GPIO.HIGH)

        if MDdata == b'"r"':
            print("right")
            GPIO.output(A1, GPIO.HIGH)
            GPIO.output(A2, GPIO.LOW)
            GPIO.output(B1, GPIO.LOW)
            GPIO.output(B2, GPIO.HIGH)

        if MDdata == b'"l"':
            print("left")
            GPIO.output(A1, GPIO.LOW)
            GPIO.output(A2, GPIO.HIGH)
            GPIO.output(B1, GPIO.HIGH)
            GPIO.output(B2, GPIO.LOW)

        if MDdata == b'"s"':
            print("stop")
            GPIO.output(A1, GPIO.LOW)
            GPIO.output(A2, GPIO.LOW)
            GPIO.output(B1, GPIO.LOW)
            GPIO.output(B2, GPIO.LOW)
    
    return render_template('new.html')
            
if __name__ == "__main__":
    rover.run(debug=True, port=8000, host='0.0.0.0')