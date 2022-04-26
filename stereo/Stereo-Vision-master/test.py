import numpy as np
import cv2

print('Starting the Calibration. Press and maintain the space bar to exit the script\n')
print('Push (s) to save the image you want and push (c) to see next frame without saving the image')

id_image=0

# termination criteria
criteria =(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Call the two cameras
CamR= cv2.VideoCapture(0)   # 0 -> Right Camera
CamL= cv2.VideoCapture(1)   # 1 -> Left Camera

while True:
    retR, frameR= CamR.read()
    retL, frameL= CamL.read()
    grayR= cv2.cvtColor(frameR,cv2.COLOR_BGR2GRAY)
    grayL= cv2.cvtColor(frameL,cv2.COLOR_BGR2GRAY)
    cv2.imshow('imgR',frameR)
    cv2.imshow('imgL',frameL)

    # Find the chess board corners

  
    # End the Programme
    if cv2.waitKey(1) & 0xFF == ord(' '):   # Push the space bar and maintan to exit this Programm
        break

# Release the Cameras
CamR.release()
CamL.release()
cv2.destroyAllWindows()    
