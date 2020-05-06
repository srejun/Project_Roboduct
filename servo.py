import RPi.GPIO as GPIO
import time

servoPINX = 20
servoPINY = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPINX, GPIO.OUT)
GPIO.setup(servoPINY, GPIO.OUT)

pX = GPIO.PWM(servoPINX, 50) # GPIO 17 for PWM with 50Hz
pY = GPIO.PWM(servoPINY, 50)
pX.start(0) # Initialization
pY.start(0)
try:
  while True:
    pX.ChangeDutyCycle(1.5)
    pY.ChangeDutyCycle(1.5)
    time.sleep(2)
    pX.ChangeDutyCycle(3)
    pY.ChangeDutyCycle(3)
    time.sleep(2)
    pX.ChangeDutyCycle(4.5)
    pY.ChangeDutyCycle(4.5)
    time.sleep(2)
    pX.ChangeDutyCycle(6)
    pY.ChangeDutyCycle(6)
    time.sleep(2)
except KeyboardInterrupt:
  pX.stop()
  pY.stop()
  GPIO.cleanup()