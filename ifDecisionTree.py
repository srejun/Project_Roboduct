#import csv
from __future__ import print_function
import numpy as np
import RPi.GPIO as GPIO
import time 
import joblib
import pickle
#from keras.models import load_model
#from sklearn import preprocessing
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

turn = 30 #power of left-right (0-100)
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
pX.start(8.5) # Initialization
pY.start(3.5)

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
        pwm4.ChangeDutyCycle(0)

def right():
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(turn)
        pwm4.ChangeDutyCycle(0)
	
def stop():
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(0)
        pwm4.ChangeDutyCycle(0)

def tree(Sensor_Left, Sensor_Right):
  if Sensor_Left <= 0.5976932644844055:
    if Sensor_Left <= 0.4694354832172394:
      if Sensor_Left <= 0.13886011391878128:
        if Sensor_Left <= 0.0795106329023838:
          #return [[ 8.  4. 45.]]
          return "right"
        else:  # if Sensor_Left > 0.0795106329023838
          #return [[49.  8. 51.]]
          return "right"
      else:  # if Sensor_Left > 0.13886011391878128
        if Sensor_Right <= 0.9190115332603455:
          #return [[13.  9. 38.]]
          return "right"
        else:  # if Sensor_Right > 0.9190115332603455
          #return [[ 27.  32. 239.]]
          return "right"
    else:  # if Sensor_Left > 0.4694354832172394
      if Sensor_Right <= 0.8714365363121033:
        if Sensor_Left <= 0.5214194655418396:
          #return [[10.  0. 23.]]
          return "right"
        else:  # if Sensor_Left > 0.5214194655418396
          #return [[26. 15. 35.]]
          return "right"
      else:  # if Sensor_Right > 0.8714365363121033
        if Sensor_Right <= 0.872230738401413:
          #return [[0. 1. 0.]]
          return "left"
        else:  # if Sensor_Right > 0.872230738401413
          #return [[10.  3.  3.]]
          return "forward"
  else:  # if Sensor_Left > 0.5976932644844055
    if Sensor_Left <= 0.8943057358264923:
      if Sensor_Left <= 0.7372100353240967:
        if Sensor_Right <= 0.8011175096035004:
          #return [[94. 45. 58.]]
          return "forward"
        else:  # if Sensor_Right > 0.8011175096035004
          #return [[0. 1. 0.]]
          return "left"
      else:  # if Sensor_Left > 0.7372100353240967
        if Sensor_Left <= 0.7404933869838715:
          #return [[0. 3. 0.]]
          return "left"
        else:  # if Sensor_Left > 0.7404933869838715
          #return [[113. 105.  35.]]
          return "forward"
    else:  # if Sensor_Left > 0.8943057358264923
      if Sensor_Left <= 0.9929430484771729:
        if Sensor_Right <= 0.25384241342544556:
          #return [[ 25. 118.   6.]]
          return "left"
        else:  # if Sensor_Right > 0.25384241342544556
          #return [[ 72. 118.  14.]]
          return "left"
      else:  # if Sensor_Left > 0.9929430484771729
        if Sensor_Left <= 0.9997735619544983:
          #return [[72. 62.  7.]]
          return "forward"
        else:  # if Sensor_Left > 0.9997735619544983
          #return [[0. 6. 3.]]
          return "left"
          
def treeExpert(Sensor_Left, Sensor_Right):
	if Sensor_Left <= 0.5976932644844055:
		if Sensor_Right <= 0.8829601109027863:
			if Sensor_Left <= 0.4905073791742325:
				if Sensor_Left <= 0.4890940636396408:
					#return [[10. 3. 3.]]
					return "forward"
				else: # if Sensor_Left &gt; 0.4890940636396408
					#return [[0. 1. 0.]]
					return "left"
			else: # if Sensor_Left &gt; 0.4905073791742325
				if Sensor_Left <= 0.5214194655418396:
					#return [[10. 0. 23.]]
					return "right"
				else: # if Sensor_Left &gt; 0.5214194655418396
					#return [[26. 15. 35.]]
					return "right"
		else: # if Sensor_Right &gt; 0.8829601109027863
			if Sensor_Left <= 0.13886011391878128:
				if Sensor_Left <= 0.0795106329023838:
					#return [[ 8. 4. 45.]]
					return "right"
				else: # if Sensor_Left &gt; 0.0795106329023838
					#return [[49. 8. 51.]]
					return "right"
			else: # if Sensor_Left &gt; 0.13886011391878128
				if Sensor_Left <= 0.3942306637763977:
					#return [[ 27. 32. 239.]]
					return "right"
				else: # if Sensor_Left &gt; 0.3942306637763977
					#return [[13. 9. 38.]]
					return "right"
	else: # if Sensor_Left &gt; 0.5976932644844055
		if Sensor_Left <= 0.8943057358264923:
			if Sensor_Right <= 0.6756618320941925:
				if Sensor_Right <= 0.6720636188983917:
					#return [[113. 105. 35.]]
					return "forward"
				else: # if Sensor_Right &gt; 0.6720636188983917
					#return [[0. 3. 0.]]
					return "left"
			else: # if Sensor_Right &gt; 0.6756618320941925
				if Sensor_Left <= 0.5985070168972015:
					#return [[0. 1. 0.]]
					return "left"
				else: # if Sensor_Left &gt; 0.5985070168972015
					#return [[94. 45. 58.]]
					return "forward"
		else: # if Sensor_Left &gt; 0.8943057358264923
			if Sensor_Right <= 0.1185920313000679:
				if Sensor_Left <= 0.9997735619544983:
					#return [[72. 62. 7.]]
					return "forward"
				else: # if Sensor_Left &gt; 0.9997735619544983
					#return [[0. 6. 3.]]
					return "left"
			else: # if Sensor_Right &gt; 0.1185920313000679
				if Sensor_Left <= 0.9672455787658691:
					#return [[ 72. 118. 14.]]
					return "left"
				else: # if Sensor_Left &gt; 0.9672455787658691
					#return [[ 25. 118. 6.]]
					return "left"
					
def treeRandom(Sensor_Left, Sensor_Right):
	if Sensor_Left <= 0.637399286031723:
		if Sensor_Left <= 0.2107377052307129:
			if Sensor_Left <= 0.07949581742286682:
				if Sensor_Left <= 0.04932686872780323:
					#return [[ 0. 4. 15.]]
					return "right"
				else: # if Sensor_Left &gt; 0.04932686872780323
					#return [[ 3. 1. 10.]]
					return "right"
			else: # if Sensor_Left &gt; 0.07949581742286682
				if Sensor_Right <= 0.9930793642997742:
					#return [[67. 7. 27.]]
					return "forward"
				else: # if Sensor_Right &gt; 0.9930793642997742
					#return [[19. 2. 16.]]
					return "forward"
		else: # if Sensor_Left &gt; 0.2107377052307129
			if Sensor_Left <= 0.44974932074546814:
				if Sensor_Right <= 0.946929544210434:
					#return [[ 5. 24. 34.]]
					return "right"
				else: # if Sensor_Right &gt; 0.946929544210434
					#return [[18. 12. 48.]]
					return "right"
			else: # if Sensor_Left &gt; 0.44974932074546814
				if Sensor_Right <= 0.8803199827671051:
					#return [[43. 36. 35.]]
					return "forward"
				else: # if Sensor_Right &gt; 0.8803199827671051
					#return [[5. 4. 0.]]
					return "forward"
	else: # if Sensor_Left &gt; 0.637399286031723
		if Sensor_Right <= 0.379143163561821:
			if Sensor_Right <= 0.038398162461817265:
				#return [[0. 2. 0.]]
				return "left"
			else: # if Sensor_Right &gt; 0.038398162461817265
				if Sensor_Left <= 0.9318716824054718:
					#return [[10. 1. 0.]]
					return "forward"
				else: # if Sensor_Left &gt; 0.9318716824054718
					#return [[89. 44. 7.]]
					return "forward"
		else: # if Sensor_Right &gt; 0.379143163561821
			if Sensor_Right <= 0.38376301527023315:
				#return [[0. 3. 0.]]
				return "left"
			else: # if Sensor_Right &gt; 0.38376301527023315
				if Sensor_Left <= 0.758815199136734:
					#return [[66. 40. 3.]]
					return "forward"
				else: # if Sensor_Left &gt; 0.758815199136734
					#return [[87. 80. 10.]]
					return "forward"

#path = "/home/pi/Desktop/Project_RoboDuct/Project/aiToauto"
#model = load_model("NeuronNetwork_Random_RoboDuct.h5" ) 
#model = joblib.load(path + 'LinearSVC_model_Preprocessing_by_Normalizer_RoboDuct.h5')
#model = joblib.load('DecisionTreeClassifier_TEST.h5')
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
	data_normal = Normalizer().fit_transform(x)
	leftnor=data_normal[0,0]
	rightnor=data_normal[0,1]
	#print(x.shape)
	#print(x)
	#PREDICTED = model.predict(X_normal)
	
	#PREDICTED=tree(leftnor,rightnor)
	PREDICTED=treeExpert(leftnor,rightnor)
	#PREDICTED=treeRandom(leftnor,rightnor)
	if(PREDICTED == "forward"):
	    forward()
	    Action = "Forward"
	elif(PREDICTED == "left"):
	    left()
	    Action = "Left"
	elif(PREDICTED == "right"):
	    right()
	    Action = "Right"
	else:
		Action = "ERROR"
	
	time.sleep(1)
	stop()
	time.sleep(2)
	
	print(Action)
	#print(data_normal)
	#print(left)
	
#0 = Forward , 1 = Left , 2 = Right 
# For NeuronNetwork [ w x y z ] , If " w " is the most Then Backward , If " x " is the most Then Forward , If " y " is the most Then Left , If " z " is the most Then Right

#Use Action for drive motor
