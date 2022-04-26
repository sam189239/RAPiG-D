import numpy as np
import cv2
from matplotlib import pyplot as plt

# Call the two cameras
CamR= cv2.VideoCapture(0)   # 0 -> Right Camera
CamL= cv2.VideoCapture(1)   # 1 -> Left Camera

while True:
    retR, frameR= CamR.read()
    retL, frameL= CamL.read()
    grayR= cv2.cvtColor(frameR,cv2.COLOR_BGR2GRAY)
    grayL= cv2.cvtColor(frameL,cv2.COLOR_BGR2GRAY)
    imgL = grayL #cv2.imread('tsukuba_l.png',0)
    imgR = grayR #cv2.imread('tsukuba_r.png',0)

    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(imgL,imgR)
    cv2.imshow('gray', disparity)
    

