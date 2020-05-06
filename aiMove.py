#import csv
from __future__ import print_function
import numpy as np
import RPi.GPIO as GPIO
import time 
import joblib
import pickle
#from keras.models import load_model
from sklearn.preprocessing import Normalizer
#from _classification import *
#from sklearn.externals import joblib

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

turn = 29 #power of left-right (0-100)
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
        pwm4.ChangeDutyCycle(turn/3)

def right():
        pwm1.ChangeDutyCycle(turn/3)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(turn)
        pwm4.ChangeDutyCycle(0)
	
def stop():
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(0)
        pwm4.ChangeDutyCycle(0)

#path = "/home/pi/Desktop/Project_RoboDuct/Project/aiToauto"
#model = load_model("NeuronNetwork_Random_RoboDuct.h5" ) 
#model = joblib.load(path + 'LinearSVC_model_Preprocessing_by_Normalizer_RoboDuct.h5')
model = joblib.load('GaussianNB_79_05_percent.h5')
#with open('GaussianNB_RoboDuct.h5','rb') as pickle_file:
 #   model = pickle.load(pickle_file)    
    
work()
    
while(True):
	distleft = distanceleft()
	distrigth = distancerigth()
	#print(distleft)
	#print(distrigth)
	x = np.array( [ [distleft],[distrigth] ] )
	#x = np.array([[4],[10]])
	x = np.transpose(x)
	X_normal = Normalizer().fit_transform(x)
	#print(x.shape)
	print(x)
	PREDICTED = model.predict(X_normal)
	if(PREDICTED == 0):
	    forward()
	    Action = "Forward"
	elif(PREDICTED == 1):
	    left()
	    Action = "Left"
	elif(PREDICTED == 2):
	    right()
	    Action = "Right"
	time.sleep(1)
	stop()
	time.sleep(2)
	print(PREDICTED)
	print(Action)
	
#0 = Forward , 1 = Left , 2 = Right 
# For NeuronNetwork [ w x y z ] , If " w " is the most Then Backward , If " x " is the most Then Forward , If " y " is the most Then Left , If " z " is the most Then Right

#Use Action for drive motor
