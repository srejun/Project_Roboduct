import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

w1 = 7
w2 = 11
w3 = 13
w4 = 15

turn = 85 #power of left-right (0-100)
run = 100  #power of forward-backward (0-100)

GPIO.setup(w1,GPIO.OUT)
GPIO.setup(w2,GPIO.OUT)
GPIO.setup(w3,GPIO.OUT)
GPIO.setup(w4,GPIO.OUT)

GPIO.setup(29,GPIO.IN)
GPIO.setup(31,GPIO.IN)
GPIO.setup(33,GPIO.IN)

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
    pwm1.ChangeDutyCycle(run)
    pwm2.ChangeDutyCycle(0)
    pwm3.ChangeDutyCycle(0)
    pwm4.ChangeDutyCycle(run)

def backward():
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(run)
        pwm3.ChangeDutyCycle(run)
        pwm4.ChangeDutyCycle(0)

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
    L = GPIO.input(29)
    C = GPIO.input(31)
    R = GPIO.input(33)

    if(L == C == R == 1 and checkword != 'none'):
        print("L=%d C=%d R=%d"%(L,C,R))
        break;
    elif(L == 0 and R == 1):
        right()
        checkword = 'right'
    elif(L == 1 and R == 0):
        left()
        checkword = 'left'
    else:
        forward()
        checkword = 'forward'

    print("L=%d C=%d R=%d"%(L,C,R))
    print(checkword)
stop()

