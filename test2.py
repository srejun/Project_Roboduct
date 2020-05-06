import cv2
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_threshold = int(max(0, (1.0 - 0.33) * median))
    upper_threshold = int(min(255, (1.0 + 0.33) * median))
    
    edges = cv2.Canny(frame,lower_threshold,upper_threshold)
    cv2.imshow('Original',frame)
    
    cv2.imshow('Edges',edges)
    
    if cv2.waitKey(20) and 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()