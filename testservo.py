import RPi.GPIO as GPIO
import time

servoPINX = 38
servoPINY = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(servoPINX, GPIO.OUT)
GPIO.setup(servoPINY, GPIO.OUT)

pX = GPIO.PWM(servoPINX, 50) # GPIO 17 for PWM with 50Hz
pY = GPIO.PWM(servoPINY, 50)
pX.start(8) # Initialization
pY.start(4)
try:
  while True:
    pX.ChangeDutyCycle(7)
    pY.ChangeDutyCycle(5)
    time.sleep(2)
    pX.ChangeDutyCycle(8)
    pY.ChangeDutyCycle(4)
    time.sleep(2)
    pX.ChangeDutyCycle(9)
    pY.ChangeDutyCycle(3)
    time.sleep(2)
except KeyboardInterrupt:
  pX.stop()
  pY.stop()
  GPIO.cleanup()