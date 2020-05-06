#Libraries
import RPi.GPIO as GPIO
import time
import numpy
import cv2
cap = cv2.VideoCapture(0)
# Define the codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,  480))

file = open("datasensor.txt","w") 

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
 
if __name__ == '__main__':
    print("Action")
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            frame = cv2.flip(frame, 0)
            # write the flipped frame
            out.write(frame)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break
            distleft = distanceleft()
            print ("Measured Distanceleft = %.1f cm" % distleft)
            distrigth = distancerigth()
            print ("Measured Distancerigth = %.1f cm" % distrigth)
            
            file.write("distLeft %.2f\r\n" %distleft)
            file.write("distRigth %.2f\r\n" %distrigth) 
            time.sleep(2)
        file.close()
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

cap.release()
out.release()
cv2.destroyAllWindows()