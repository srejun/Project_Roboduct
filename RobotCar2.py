
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

w1 = 7
w2 = 11
w3 = 13
w4 = 15
toggle = 1
status = 0
turn = 80 #power of left-right (0-100)
run = 35  #power of forward-backward (0-100)
t=time.sleep(0.2)

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
#0 = black ,,,,,,,,,,,,,,, 1 = white
    if(L==0 and R==1):
        status = 1
        print("right")
        """while(status==1):
            L = GPIO.input(29)
                C = GPIO.input(31)
                R = GPIO.input(33)
            if(R==0):
                status=0"""
        if(checkword=='left'): 
            print("Cannot turn")
            forward()
            checkword = 'forward'
        else:
            right()
            checkword = 'right'
    elif(L==1 and R==0):
        status = 0
        print("left")
        """while(status==0):
            L = GPIO.input(29)
                C = GPIO.input(31)
                R = GPIO.input(33)
            if(L==0):
                status=1"""
        if(checkword=='right'): 
            print("Cannot turn")
            forward()
            checkword = 'forward'
        else:
            left()
            checkword = 'left'
    #if(L==1 and R==1):
    #   right()
    #   checkword = '2 ways go right'
    elif(C==L==R==1 or (L==0 and C==1 and R==0)):
        forward()
        checkword = 'forward'
    elif(C==L==R==0):
        if(checkword=='forward'): 
                        forward()
            checkword = 'forward'
                elif(checkword=='left'): 
                        left()
                        checkword = 'left'
                elif(checkword=='right'): 
                        right()
                        checkword = 'right'

    else:
        if(checkword=='forward'): 
            forward()
            checkword = 'forward'
        elif(checkword=='left'): 
            left()
            checkword = 'left'
        elif(checkword=='right'): 
            right()
            checkword = 'right'
    print("L=%d C=%d R=%d"%(L,C,R))
    print(checkword)
#   time.sleep(0.05)
