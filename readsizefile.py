import numpy as np
import cv2
img = cv2.imread('capture.jpg')
height = img.shape[0]
width = img.shape[1]
channels = img.shape[2]
 

print('Image Height       : ',height)
print('Image Width        : ',width)
print('Number of Channels : ',channels)