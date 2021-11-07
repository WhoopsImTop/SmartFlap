from components.drawOnImage import *
from components.pushNotifier import *

from picamera import PiCamera
import subprocess
import logging
import json
import time

#Kamera Aktivieren und Push Service Registrieren
camera = PiCamera()
camera.resolution = (640, 480)

#setup Logging
logging.basicConfig(filename="server/Katze.log", filemode="w", format='%(asctime)s - %(message)s', level=logging.INFO)

def movementDetected():
    # Hier kann alternativ eine Anwendung/Befehl etc. gestartet werden.
    logging.info("Es gab eine Bewegung")
    camera.start_preview()
    camera.capture('/home/pi/Desktop/SmartFlap/static/pictures/picture.jpg')
    camera.stop_preview()
    response = subprocess.check_output(['node', '././predict.js'])
    parsed = json.loads(response)
    if(parsed.find("Katze") == 0):
        DrawOnImg(parsed, "picture-named.jpg")
        pushNotify()
        logging.info("Bild wurde gesendet Katze")
    elif(parsed.find("Mit Maus") == 0):
        DrawOnImg(parsed, "picture-named.jpg")
        pushNotify()
        logging.info("Bild wurde gesendet Mit Maus")
        time.sleep(60)
    else:
        DrawOnImg(" ", "picture.jpg")
    time.sleep(10)
