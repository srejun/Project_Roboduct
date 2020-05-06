import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


w1 = 31
w2 = 33
w3 = 35
w4 = 37
w5 = 5
w6 = 7

servoPINleft = 38
servoPINright = 40

turn = 29 #power of left-right (0-100)
run = 84  #power of forward-backward (0-100)
#t=time.sleep(0.2)

GPIO.setup(w1,GPIO.OUT)
GPIO.setup(w2,GPIO.OUT)
GPIO.setup(w3,GPIO.OUT)
GPIO.setup(w4,GPIO.OUT)
GPIO.setup(w5,GPIO.OUT)
GPIO.setup(w6,GPIO.OUT)

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
action='none'

def work():
    pwm5.ChangeDutyCycle(0)
    pwm6.ChangeDutyCycle(run)
    

while(True):
    work()
