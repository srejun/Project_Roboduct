#Libraries
from __future__ import print_function
import RPi.GPIO as GPIO
import time
import xbox

file = open("cleaningdata.txt","w") 

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
 
#set GPIO Pins
GPIO_TRIGGERleft = 12
GPIO_ECHOleft = 16
GPIO_TRIGGERrigth = 24
GPIO_ECHOrigth = 26
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGERleft, GPIO.OUT)
GPIO.setup(GPIO_ECHOleft, GPIO.IN)
GPIO.setup(GPIO_TRIGGERrigth, GPIO.OUT)
GPIO.setup(GPIO_ECHOrigth, GPIO.IN)

w1 = 31
w2 = 33
w3 = 35
w4 = 37
w5 = 5
w6 = 7

servoPINleft = 38
servoPINright = 40

turn = 27 #power of left-right (0-100)
run = 34  #power of forward-backward (0-100)
works = 100
#t=time.sleep(0.2)

GPIO.setup(w1,GPIO.OUT)
GPIO.setup(w2,GPIO.OUT)
GPIO.setup(w3,GPIO.OUT)
GPIO.setup(w4,GPIO.OUT)
GPIO.setup(w5,GPIO.OUT)
GPIO.setup(w6,GPIO.OUT)

GPIO.setup(servoPINleft, GPIO.OUT)
GPIO.setup(servoPINright, GPIO.OUT)

pX = GPIO.PWM(servoPINleft, 50) # GPIO 17 for PWM with 50Hz
pY = GPIO.PWM(servoPINright, 50)
pX.start(8) # Initialization
pY.start(4)

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
    pwm6.ChangeDutyCycle(works)

def forward():
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(run+2)
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

def lefthight():
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(turn*1.5)
        pwm3.ChangeDutyCycle(0)
        pwm4.ChangeDutyCycle(turn*1.5)

def righthight():
        pwm1.ChangeDutyCycle(turn*1.5)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(turn*1.5)
        pwm4.ChangeDutyCycle(0)

def stop():
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(0)
        pwm4.ChangeDutyCycle(0)

# Format floating point number to string format -x.xxx
def fmtFloat(n):
    return '{:6.3f}'.format(n)

# Print one or more values without a line feed
def show(*args):
    for arg in args:
        print(arg, end="")

# Print true or false value based on a boolean, without linefeed
def showIf(boolean, ifTrue, ifFalse=" "):
    if boolean:
        show(ifTrue)
    else:
        show(ifFalse)

# Instantiate the controller
joy = xbox.Joystick()

# Show various axis and button states until Back button is pressed
print("Xbox controller sample: Press Back button to exit")
 
def distanceleft():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGERleft, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGERleft, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHOleft) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHOleft) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def distancerigth():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGERrigth, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGERrigth, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHOrigth) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHOrigth) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    #print("Action")
    try:
        work()
        while not joy.Back():
            #work()
            action='none'
            # Show connection status
        #    show("Connected:")
        #    showIf(joy.connected(), "Y", "N")
            # Left analog stick
        #    show("  Left X/Y:", fmtFloat(joy.leftX()), "/", fmtFloat(joy.leftY()))
            # Right trigger
        #    show("  RightTrg:", fmtFloat(joy.rightTrigger()))
            # A/B/X/Y buttons
            show("  Buttons:")
            showIf(joy.A(), "A")
        #    if(joy.A()==1):
            showIf(joy.B(), "B")
            showIf(joy.X(), "X")
            showIf(joy.Y(), "Y")
            if(joy.A()==1):
#                pX.ChangeDutyCycle(7.2)
#                pY.ChangeDutyCycle(4.8)
#                show("down")
                backward()
                time.sleep(1)
                stop()
                action='backward'
        #        time.sleep(1)
            elif(joy.Y()==1):
#                pX.ChangeDutyCycle(9)
#                pY.ChangeDutyCycle(3)
#                show("up")
                forward()
                time.sleep(1)
                stop()
                action='forward'
        #        time.sleep(1)
            elif(joy.X()==1):
                left()
                time.sleep(1)
                stop()
                action='left'
            elif(joy.B()==1):
                right()
                time.sleep(1)
                stop()
                action='right'
            # Dpad U/D/L/R
            show("  Dpad:")
            showIf(joy.dpadUp(),    "U")
            showIf(joy.dpadDown(),  "D")
            showIf(joy.dpadLeft(),  "L")
            showIf(joy.dpadRight(), "R")
            if(joy.dpadUp()==1):
#                forward()
#                time.sleep(1)
#                stop()
#                action='forward'
                pX.ChangeDutyCycle(9)
                pY.ChangeDutyCycle(3)
                show("up")
            elif(joy.dpadDown()==1):
                pX.ChangeDutyCycle(8.0)
                pY.ChangeDutyCycle(4.0)
                show("down")
#                backward()
#                time.sleep(1)
#                stop()
#                action='backward'
            elif(joy.dpadLeft()==1):
                show("")
#                left()
#                time.sleep(1)
#                stop()
#                action='left'
            elif(joy.dpadRight()==1):
                show("")
#                right()
#                time.sleep(1)
#                stop()
#                action='right'
            # Move cursor back to start of line
            show(chr(13))
            distleft = distanceleft()
            print ("Distanceleft = %.1f cm" % distleft)
            distrigth = distancerigth()
            print ("Distancerigth = %.1f cm" % distrigth)
            print ("action = %s" %action)
            time.sleep(2)
            file.write("distLeft %.2f\r\n" %distleft)
            file.write("distRigth %.2f\r\n" %distrigth)
            file.write("action %s\r\n" %action)
        # Close out when done
        joy.close()
        file.close()
        
#        while True:
#            
#            distleft = distanceleft()
#            print ("Measured Distanceleft = %.1f cm" % distleft)
#            distrigth = distancerigth()
#            print ("Measured Distancerigth = %.1f cm" % distrigth)
#            time.sleep(2)
#            file.write("distLeft %.2f\r\n" %distleft)
#            file.write("distRigth %.2f\r\n" %distrigth) 
##            time.sleep(2)
#            print("Action")
#        file.close()
        # Reset by pressing CTRL + C
    
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

