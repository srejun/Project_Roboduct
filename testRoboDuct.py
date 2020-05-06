
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

w1 = 31
w2 = 33
w3 = 35
w4 = 37
toggle = 1
status = 0
turn = 40 #power of left-right (0-100)
run = 40  #power of forward-backward (0-100)
t=time.sleep(0.2)

GPIO.setup(w1,GPIO.OUT)
GPIO.setup(w2,GPIO.OUT)
GPIO.setup(w3,GPIO.OUT)
GPIO.setup(w4,GPIO.OUT)

#GPIO.setup(29,GPIO.IN)
#GPIO.setup(31,GPIO.IN)
#GPIO.setup(33,GPIO.IN)

pwm1 = GPIO.PWM(w1,120) # FL
pwm2 = GPIO.PWM(w2,120) # BL
pwm3 = GPIO.PWM(w3,120) # BR
pwm4 = GPIO.PWM(w4,120) # FR

pwm1.start(0)
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)
checkword = 'none'

def forward():
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(run)
    pwm3.ChangeDutyCycle(run)
    pwm4.ChangeDutyCycle(0)

def backward():
        pwm1.ChangeDutyCycle(run)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(0)
        pwm4.ChangeDutyCycle(run)

def left():
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(turn)
        pwm3.ChangeDutyCycle(0)
        pwm4.ChangeDutyCycle(turn)

def right():
        pwm1.ChangeDutyCycle(turn)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(turn)
        pwm4.ChangeDutyCycle(0)

def stop():
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(0)
        pwm4.ChangeDutyCycle(0)

while(True):
    i=0
    while(i<5000):
        forward()
        i=i+1;
    i=0
    time.sleep(0.5)
    while(i<5000):
        backward()
        i=i+1;
    i=0
    time.sleep(0.5)
    while(i<5000):
        left()
        i=i+1;
    i=0
    time.sleep(0.5)
    while(i<5000):
        right()
        i=i+1;
    i=0
    time.sleep(0.5)
    while(i<5000):
        stop()
        i=i+1
    time.sleep(0.5)

