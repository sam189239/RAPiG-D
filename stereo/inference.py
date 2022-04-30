import cv2
import numpy as np


def coords_mouse_disp(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        #print x,y,disp[y,x],filteredImg[y,x]
        average=0
        for u in range (-1,2):
            for v in range (-1,2):
                average += disp[y+u,x+v]
        average=average/9
        Distance= -593.97*average**(3) + 1506.8*average**(2) - 1373.1*average + 522.06
        Distance= np.around(Distance*0.01,decimals=2)
        print('Distance: '+ str(Distance)+' m')

alpha = 55
kernel= np.ones((3,3),np.uint8)

chessboardSize = (10,7)
frameSize = (640,480)
base_len = 8

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

num = 0

cv_file = cv2.FileStorage()
cv_file.open('stereoMap_old.xml', cv2.FileStorage_READ)

stereomap_l_x = cv_file.getNode('stereoMapL_x').mat()
stereomap_l_y = cv_file.getNode('stereoMapL_y').mat()
stereomap_r_x = cv_file.getNode('stereoMapR_x').mat()
stereomap_r_y = cv_file.getNode('stereoMapR_y').mat()

# stereo = cv2.StereoBM_create()

# Create StereoSGBM and prepare all parameters
window_size = 3
min_disp = 2
num_disp = 130-min_disp
stereo = cv2.StereoSGBM_create(minDisparity = min_disp,
    numDisparities = num_disp,
    blockSize = window_size,
    uniquenessRatio = 10,
    speckleWindowSize = 100,
    speckleRange = 32,
    disp12MaxDiff = 5,
    P1 = 8*3*window_size**2,
    P2 = 32*3*window_size**2)

# Used for the filtered image
stereoR=cv2.ximgproc.createRightMatcher(stereo) # Create another stereo for right this time

# WLS FILTER Parameters
lmbda = 80000
sigma = 1.8
visual_multiplier = 1.0
 
wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=stereo)
wls_filter.setLambda(lmbda)
wls_filter.setSigmaColor(sigma)

while cap.isOpened():

    succes1, img = cap.read()
    succes2, img2 = cap2.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    frameR = cv2.remap(img2, stereomap_r_x, stereomap_r_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    frameL = cv2.remap(img, stereomap_l_x, stereomap_l_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)


    # CONVERT FOCAL LENGTH f FROM [mm] TO [pixel]:
    height_right, width_right = frameR.shape
    height_left, width_left = frameL.shape

    if width_right == width_left:
        f_pixel = (width_right * 0.5) / np.tan(alpha * 0.5 * np.pi/180)
        # print(f_pixel)
    else:
        print('Left and right camera frames do not have the same pixel width')

    disp= stereo.compute(frameL,frameR)#.astype(np.float32)/ 16
    dispL= disp
    dispR= stereoR.compute(frameR,frameL)
    dispL= np.int16(dispL)
    dispR= np.int16(dispR)

    # Using the WLS filter
    filteredImg= wls_filter.filter(dispL,frameL,None,dispR)
    filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
    filteredImg = np.uint8(filteredImg)
    cv2.imshow('Disparity Map', filteredImg)
    disp= ((disp.astype(np.float32)/ 16)-min_disp)/num_disp # Calculation allowing us to have 0 for the most distant object able to detect

    depth = base_len * f_pixel / filteredImg
    cv2.imshow('depth', depth)

##    # Resize the image for faster executions
##    dispR= cv2.resize(disp,None,fx=0.7, fy=0.7, interpolation = cv2.INTER_AREA)

    # Filtering the Results with a closing filter
    closing= cv2.morphologyEx(disp,cv2.MORPH_CLOSE, kernel) # Apply an morphological filter for closing little "black" holes in the picture(Remove noise) 


    # Colors map
    dispc= (closing-closing.min())*255
    dispC= dispc.astype(np.uint8)                                   # Convert the type of the matrix from float32 to uint8, this way you can show the results with the function cv2.imshow()
    disp_Color= cv2.applyColorMap(dispC,cv2.COLORMAP_JET)         # Change the Color of the Picture into an Ocean Color_Map
    filt_Color= cv2.applyColorMap(filteredImg,cv2.COLORMAP_JET) 
    
    # Show the result for the Depth_image
    #cv2.imshow('Disparity', disp)
    #cv2.imshow('Closing',closing)
    #cv2.imshow('Color Depth',disp_Color)
    cv2.imshow('Filtered Color Depth',filt_Color)

    # Mouse click
    cv2.setMouseCallback("Filtered Color Depth",coords_mouse_disp,filt_Color)
    
    # End the Programme
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break
    
# Save excel
##wb.save("data4.xlsx")


