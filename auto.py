import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
#GPIO.setmode(GPIO.BCM)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#set GPIO Pins
GPIO_TRIGGER_left = 12
GPIO_ECHO_left = 16
GPIO_TRIGGER_forward = 18
GPIO_ECHO_forward = 22
GPIO_TRIGGER_right = 24
GPIO_ECHO_right = 26
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER_left, GPIO.OUT)
GPIO.setup(GPIO_ECHO_left, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_forward, GPIO.OUT)
GPIO.setup(GPIO_ECHO_forward, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_right, GPIO.OUT)
GPIO.setup(GPIO_ECHO_right, GPIO.IN)

servoPINX = 38
servoPINY = 40

w1 = 31
w2 = 33
w3 = 35
w4 = 37
toggle = 1
status = 0
turn = 35 #power of left-right (0-100)
run = 35  #power of forward-backward (0-100)
t=time.sleep(0.2)

GPIO.setup(w1,GPIO.OUT)
GPIO.setup(w2,GPIO.OUT)
GPIO.setup(w3,GPIO.OUT)
GPIO.setup(w4,GPIO.OUT)

GPIO.setup(servoPINX, GPIO.OUT)
GPIO.setup(servoPINY, GPIO.OUT)

pX = GPIO.PWM(servoPINX, 50) # GPIO 17 for PWM with 50Hz
pY = GPIO.PWM(servoPINY, 50)
pX.start(8) # Initialization
pY.start(4)

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
 
def distance_left():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER_left, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_left, False)
 
    StartTime_left = time.time()
    StopTime_left = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO_left) == 0:
        StartTime_left = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO_left) == 1:
        StopTime_left = time.time()
 
    # time difference between start and arrival
    TimeElapsed_left = StopTime_left - StartTime_left
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance_left = (TimeElapsed_left * 34300) / 2
    return distance_left

def distance_forward():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER_forward, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_forward, False)

    StartTime_forward = time.time()
    StopTime_forward = time.time()
    
    # save StartTime
    while GPIO.input(GPIO_ECHO_forward) == 0:
        StartTime_forward = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO_forward) == 1:
        StopTime_forward = time.time()
 
    # time difference between start and arrival
    TimeElapsed_forward = StopTime_forward - StartTime_forward
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance_forward = (TimeElapsed_forward * 34300) / 2 
    return distance_forward

def distance_right():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER_right, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_right, False)

    StartTime_right = time.time()
    StopTime_right = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO_right) == 0:
        StartTime_right = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO_right) == 1:
        StopTime_right = time.time()
 
    # time difference between start and arrival
    TimeElapsed_right = StopTime_right - StartTime_right
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance_right = (TimeElapsed_right * 34300) / 2
    return distance_right

while(True):
    try:
        while True:
            dist_left = distance_left()
#            dist_forward = distance_forward()
            dist_right = distance_right()
            
            pX.ChangeDutyCycle(7)
            pY.ChangeDutyCycle(5)
            time.sleep(2)
            pX.ChangeDutyCycle(8)
            pY.ChangeDutyCycle(4)
            time.sleep(2)
            pX.ChangeDutyCycle(9)
            pY.ChangeDutyCycle(3)
            time.sleep(2)
            
            print ("Distance left = %.1f cm" % dist_left)
#            print ("Distance forward = %.1f cm" % dist_forward)
            print ("Distance right = %.1f cm" % dist_right)
            
            if(dist_left>=10 and dist_right>=15):
                i=0
                while(i<80000):
                    forward()
                    i=i+1;
                stop()
                time.sleep(1)
#            print ("Distance left = %.1f cm" % dist_left)
            if(dist_left<10):
                i=0
                while(i<50000):
                    right()
                    i=i+1;
                stop()
                time.sleep(1)
#            print ("Distance forward = %.1f cm" % dist_forward)
            
            if(dist_right<10):
                i=0
                while(i<50000):
                    left()
                    i=i+1;
                stop()
                time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        pX.stop()
        pY.stop()
        print("Measurement stopped by User")
        GPIO.cleanup()
#    i=0
#    while(i<5000):
#        forward()
#        i=i+1;
#    i=0
#    time.sleep(0.5)
