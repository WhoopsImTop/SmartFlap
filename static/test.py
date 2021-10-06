import RPi.GPIO as GPIO
import time

from picamera import PiCamera
import os
import subprocess
import json
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from pushnotifier import PushNotifier as pn

#Kamera Aktivieren und Push Service Registrieren
camera = PiCamera()
camera.resolution = (640, 480)
pn = pn.PushNotifier('Elias4711', 'Anton17032000', 'katzenklappe', 'V2VBBV466C3V8E7DV2VBV2VB63CVDE7DFFBFKFTFFB')

#SetupServo
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

#SetupBewegungsmelder 
SENSOR_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)
p = GPIO.PWM(servoPIN, 50)
p.start(2.5) # Initialisierung

def TriggerServo():
    try:
        p.ChangeDutyCycle(7.5)
        time.sleep(20)
        p.ChangeDutyCycle(1)
    except:
        print("can't Open")
    GPIO.cleanup()

def pushNotify():
    pn.send_image('/home/pi/Desktop/tfjs-customvision/static/pictures/picture-named.jpg', silent=False, devices=['vgWm'])
 
def mein_callback(channel):
    # Hier kann alternativ eine Anwendung/Befehl etc. gestartet werden.
    print('Es gab eine Bewegung!')
    camera.start_preview()
    camera.capture('/home/pi/Desktop/tfjs-customvision/static/pictures/picture.jpg')
    camera.stop_preview()               
    response = subprocess.check_output(['node', './predict.js'])
    parsed = json.loads(response)
    if(parsed.find("Katze") == 0):
        TriggerServo();
    img = Image.open('/home/pi/Desktop/tfjs-customvision/static/pictures/picture.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/home/pi/Downloads/Poppins-Bold.ttf", 25)
    draw.text((50, 50), parsed, (242,186,34), font=font)
    img.save('/home/pi/Desktop/tfjs-customvision/static/pictures/picture-named.jpg')
    pushNotify();
    print("Bild wurde gesendet")
 
try:
    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=mein_callback)
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print("Beende...")
GPIO.cleanup()