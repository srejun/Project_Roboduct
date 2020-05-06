import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
#    if ret is True:
#        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#    else:
#        continue
    
    #gray display is gray and white
#    cv2.imshow('frame',gray)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()