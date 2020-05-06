import cv2

#read file image from folder /webcam (same locate this file )
#value 0 is white gray , 1 is color
img = cv2.imread('lena.png',0)
print(img)


#open window file image and destroy it
cv2.imshow('image',img)
cv2.waitKey(5000)
cv2.destroyAllWindows()