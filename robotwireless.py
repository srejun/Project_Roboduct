from __future__ import print_function
import xbox
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
turn = 26 #power of left-right (0-100)
run = 30  #power of forward-backward (0-100)
runslow = 28
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
    pwm2.ChangeDutyCycle(runslow)
    pwm3.ChangeDutyCycle(run)
    pwm4.ChangeDutyCycle(0)

def backward():
        pwm1.ChangeDutyCycle(runslow)
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

while not joy.Back():
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
    # Dpad U/D/L/R
    show("  Dpad:")
    showIf(joy.dpadUp(),    "U")
    showIf(joy.dpadDown(),  "D")
    showIf(joy.dpadLeft(),  "L")
    showIf(joy.dpadRight(), "R")
    if(joy.dpadUp()==1):
        forward()
        time.sleep(1)
        stop()
    elif(joy.dpadDown()==1):
        backward()
        time.sleep(1)
        stop()
    elif(joy.dpadLeft()==1):
        left()
        time.sleep(1)
        stop()
    elif(joy.dpadRight()==1):
        right()
        time.sleep(1)
        stop()
    # Move cursor back to start of line
    show(chr(13))
# Close out when done
joy.close()
