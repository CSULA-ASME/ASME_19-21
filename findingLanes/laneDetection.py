import cv2
import numpy as np

#Edge Detection : Identifying sharp changes in intensity in adjacent pixels
# [0,0,255,255]
# [0,0,255,255]    this is a sharp change becuase its black ( the value 0 ) and then its white ( the value 255)
# [0,0,255,255]
#
# Image can be read as a matrix of pixels

#Reads Img from the file 
image = cv2.imread('test_image.jpg')

#Step 1: Turn orginal image into grayscale image
#make a copy to keep orginal from changing
lane_image = np.copy(image)
gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)

#Step 2: Apply Gaussian Blue to image 
#       1. Convert Image to Grayscale 
#       2. Reduce Noise 
blur = cv2.GaussianBlur(gray, (5, 5), 0)
#
#[255, 255, 255]            [255, 255, 255]
#[255, 90 , 255]    ---->   [255, 185, 255]
#[255, 255, 255]            [255, 255, 255]
#
# (5, 5) --> the size of the kernel being passed over the image 

#Step 3: Canny filter on image which will apply a gaussian blur as well so step2 was for introducing gaussian blur
#Canny will perform a deerivative on both x and y axis of our images 
# a large derivative can be see as a large change in pixel intensity
# ie: [0, 255] 
# where as a small derivative can be see as a small change in pixel intensity
# ie: [0,0]

# cv2.Canny(image, low_threshold, high_threshold)
canny = cv2.Canny(blur, 50, 150)


#render image
cv2.imshow('result', image)
cv2.imshow('grayscale', gray)

cv2.imshow('blur', blur)
cv2.imshow('canny', canny)

# displays image for infinite amount of time until you click something on the keyboard
cv2.waitKey(0)
