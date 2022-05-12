import numpy as np
from matplotlib import pyplot as plt
import freenect
import cv2 as cv

def get_vid():
    array, _ = freenect.sync_get_video()
    array = cv.cvtColor(array, cv.COLOR_RGB2BGR)
    return array
    
    
while True:
    frame = get_vid()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower = np.array([0,0,70])
    upper = np.array([255, 255, 100])
    mask = cv.inRange(hsv, lower, upper)
    cv.imshow("mask",mask)
    cv.waitKey()
