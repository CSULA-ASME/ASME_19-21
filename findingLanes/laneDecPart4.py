import cv2 
import numpy as np 
import matplotlib.pyplot as plt

#Step 4: Region of Interest

def canny(laneimage):
    gray = cv2.cvtColor(laneimage, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny


def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]
        ])
    
    #np.zeros_like = creates a new array of the same size of the image but will be all set to 0 pixel values
    mask = np.zeros_like(image)

    #
    cv2.fillPoly(mask, polygons, 255)
    #Step 5: Bitwise_and
    #Takes both the mask and the canny image and runs bitwise on it, so compares the values of each 
    # pixels and if the bitwise is equal to 1 then it keeps it
    # if the bitwise is zero it masks that part of the image
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image 





#Step 6: Hough Transform
#
#
def display_line(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1,y1), (x2,y2), (255, 0, 0), 10)
    
    return line_image


#1:13:00
def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (3/5))
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return np.array([x1, y1, x2, y2])



# 1:07:00
def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2), (y1,y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
        
    left_fit_avg = np.average(left_fit, axis= 0)
    right_fit_avg = np.average(right_fit, axis= 0)

    print(left_fit_avg, 'left')
    print(right_fit_avg, 'right')

    left_line = make_coordinates(image, left_fit_avg)
    right_line = make_coordinates(image, right_fit_avg)

    return np.array([left_line, right_line])




cap = cv2.VideoCapture('test2.mp4')

while(cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength = 40, maxLineGap = 5)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_line(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

    cv2.imshow('Lane-Detection', combo_image)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()