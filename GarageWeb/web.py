import time
from datetime import datetime
from flask import Flask, render_template, request

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)  # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP) # set up pin 18 as an input with a pull-up resistor
GPIO.setup(16, GPIO.OUT) # set up pin 18 as output for the relay

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
        if GPIO.input(18) == GPIO.HIGH:
            print ("Garage is Closed")
            return app.send_static_file('Closed.html')
        else:
            print ("Garage is Open")
            return app.send_static_file('Open.html')


@app.route('/Garage', methods=['GET', 'POST'])
def Garage():
        name = request.form['garagecode']
        if name == '1234':  # 1234 is the Password that Opens Garage Door (Code if Password is Correct)
                GPIO.output(16, GPIO.LOW)
                time.sleep(1)
                GPIO.output(16, GPIO.HIGH)
                time.sleep(17)

                if GPIO.input(18) == GPIO.HIGH:
                    print ("Garage is Closed")
                    return app.send_static_file('Closed.html')
                else:
                    print ("Garage is Open")
                    return app.send_static_file('Open.html')

        if name != '1234':  # 1234 is the Password that Opens Garage Door (Code if Password is Incorrect)
                if name == "":
                        name = "NULL"
                print("Garage Code Entered: " + name)
                if GPIO.input(18) == GPIO.HIGH:
                    print ("Garage is Closed")
                    return app.send_static_file('Closed.html')
                else:
                    print ("Garage is Open")
                    return app.send_static_file('Open.html')

@app.route('/stylesheet.css')
def stylesheet():
    return app.send_static_file('stylesheet.css')


@app.route('/Log')
def logfile():
    return app.send_static_file('log.txt')


@app.route('/images/<picture>')
def images(picture):
    return app.send_static_file('images/' + picture)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)