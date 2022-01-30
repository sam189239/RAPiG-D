#!/usr/bin/env python
import freenect
import cv2
from demo import frame_convert2
import numpy as np

alert_thresh = 0.15
threshold = 150
current_depth = 450
height = 480
width = 640
roi_val = 0.25

ROI = [(int(width * roi_val), int(height * roi_val)), (int(width * (1-roi_val)), int(height * (1-roi_val)))]

def change_threshold(value):
    global threshold
    threshold = value


def change_depth(value):
    global current_depth
    current_depth = value

def check_if_object(frame):
    area = int((1 - 2*roi_val) * height * (1 - 2*roi_val) * width)
    pixels = int(np.sum(frame[ROI[0][1]:ROI[1][1], ROI[0][0]:ROI[1][0], 0]) / 255)
    return pixels > (area * alert_thresh)

def show_depth(): ## 640x480
    global threshold
    global current_depth

    depth, timestamp = freenect.sync_get_depth()
    depth = 255 * np.logical_and(depth >= 0,
                                 depth <= current_depth + threshold)
    depth = depth.astype(np.uint8)
    depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)

    is_obj = check_if_object(depth)
    if is_obj: color = (0, 0, 255)
    else: color = (0, 255, 0)
    
    frame = cv2.rectangle(depth, ROI[0], ROI[1], color, 1)
    
    
    cv2.imshow('Depth', frame)



def show_video():
    cv2.imshow('Video', frame_convert2.video_cv(freenect.sync_get_video()[0]))


cv2.namedWindow('Depth')
cv2.namedWindow('Video')
#cv2.createTrackbar('threshold', 'Depth', threshold,     500,  change_threshold)
#cv2.createTrackbar('depth',     'Depth', current_depth, 2048, change_depth)


print('Press ESC in window to stop')


while 1:
    show_depth()
    show_video()
    if cv2.waitKey(10) == 27:
        break