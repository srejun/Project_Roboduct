#import csv
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

#path = "/home/pi/Desktop/Project_RoboDuct/Project/aiToauto"
#model = load_model("NeuronNetwork_Random_RoboDuct.h5" ) 
#model = joblib.load(path + 'LinearSVC_model_Preprocessing_by_Normalizer_RoboDuct.h5')
#model = joblib.load('SGDClassifier_TEST.h5')
with open('GaussianNB_TEST.h5','rb') as pickle_file:
    model = pickle.load(pickle_file)    
x = np.array( [ [66.69],[15.39] ] )
#x = np.array([5.01,4.01])
x = np.transpose(x)
#print(x.shape)
print(x)
PREDICTED = model.predict(x)
if(PREDICTED == 0):
  Action = "Forward"
elif(PREDICTED == 1):
  Action = "Left"
elif(PREDICTED == 2):
  Action = "Right"
print(PREDICTED)
print(Action)

#0 = Forward , 1 = Left , 2 = Right 
# For NeuronNetwork [ w x y z ] , If " w " is the most Then Backward , If " x " is the most Then Forward , If " y " is the most Then Left , If " z " is the most Then Right

#Use Action for drive motor
