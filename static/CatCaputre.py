from components.movementDetected import *

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(25, GPIO.IN)

if __name__ == '__main__':
    try:
        # wait for sensor trigger loop
        while True:
            # waiting for item
            while GPIO.input(25) == 0:
                time.sleep(0.1)
                movementDetected()
            
            # waiting for item to pass
            while GPIO.input(25) == 1:
                time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()
