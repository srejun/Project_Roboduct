
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

w1 = 7
w2 = 11
w3 = 13
w4 = 15
w5 = 5
w6 = 7
toggle = 1
status = 0
turn = 50 #power of left-right (0-100)
run = 50  #power of forward-backward (0-100)
t=time.sleep(0.2)

GPIO.setup(w1,GPIO.OUT)
GPIO.setup(w2,GPIO.OUT)
GPIO.setup(w3,GPIO.OUT)
GPIO.setup(w4,GPIO.OUT)
GPIO.setup(w5,GPIO.OUT)
GPIO.setup(w6,GPIO.OUT)

GPIO.setup(29,GPIO.IN)
GPIO.setup(31,GPIO.IN)
GPIO.setup(33,GPIO.IN)

pwm1 = GPIO.PWM(w1,120) # FL
pwm2 = GPIO.PWM(w2,120) # BL
pwm3 = GPIO.PWM(w3,120) # BR
pwm4 = GPIO.PWM(w4,120) # FR
pwm5 = GPIO.PWM(w5,120)
pwm6 = GPIO.PWM(w6,120)

pwm1.start(0)
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)
pwm5.start(0)
pwm6.start(0)
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
        pwm1.ChangeDutyCycle(turn)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(turn)
        pwm4.ChangeDutyCycle(0)

def right():
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(turn)
        pwm3.ChangeDutyCycle(0)
        pwm4.ChangeDutyCycle(turn)

def stop():
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(0)
        pwm4.ChangeDutyCycle(0)
        
def work():
    pwm5.ChangeDutyCycle(0)
    pwm6.ChangeDutyCycle(run)

while(True):
    i=0
    


