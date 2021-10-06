import RPi.GPIO as GPIO
import time
import logging

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

#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#GPIO Pins zuweisen
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#setup Logging
logging.basicConfig(filename="server/Katze.log", filemode="w", format='%(asctime)s - %(message)s', level=logging.INFO)

def pushNotify():
	pn.send_image('/home/pi/Desktop/tfjs-customvision/static/pictures/picture-named.jpg', silent=False, devices=['vgWm'])

def DrawOnImg(parsed, abstand, fileName):
	detection = parsed or " "
	print(abstand)
	img = Image.open('/home/pi/Desktop/tfjs-customvision/static/pictures/picture.jpg')
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("/home/pi/Downloads/Poppins-Bold.ttf")
	draw.text((50,50), detection,(242,186,34), font=font)
	draw.text((470, 430), "SmartFlap | Elias Englen", (242,186,34), font=font)
	img.save('/home/pi/Desktop/tfjs-customvision/static/pictures/' + fileName)

def BewegungErkannt(abstand):
    # Hier kann alternativ eine Anwendung/Befehl etc. gestartet werden.
    logging.info("Es gab eine Bewegung")
    camera.start_preview()
    camera.capture('/home/pi/Desktop/tfjs-customvision/static/pictures/picture.jpg')
    camera.stop_preview()
    abstand_value = str(abstand)
    response = subprocess.check_output(['node', './predict.js'])
    parsed = json.loads(response)
    if(parsed.find("Katze") == 0):
        DrawOnImg(parsed, abstand_value, "picture-named.jpg")
        pushNotify()
        logging.info("Bild wurde gesendet Katze")
    elif(parsed.find("Mit Maus") == 0):
        DrawOnImg(parsed, abstand_value, "picture-named.jpg")
        pushNotify()
        logging.info("Bild wurde gesendet Mit Maus")
        time.sleep(60)
    else:
        DrawOnImg(" ", abstand_value, "picture.jpg")
    time.sleep(10)

def distanz():
    # setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartZeit = time.time()
    StopZeit = time.time()
 
    # speichere Startzeit
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()
 
    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()
 
    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz = (TimeElapsed * 34300) / 2
 
    return distanz

if __name__ == '__main__':
    try:
        while True:
            abstand = distanz()
            if(abstand < 50):
                BewegungErkannt(abstand)
            time.sleep(0.5)
 
        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()
