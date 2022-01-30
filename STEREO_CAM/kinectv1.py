import freenect
import cv2
import numpy as np

def get_vid():
	array, _ = freenect.sync_get_video()
	array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
	return array
	
def get_depth():
	array, _ = freenect.sync_get_depth()
	array = array.astype(np.uint8)
	return array
	
def watershed(frame):
	ret, thresh = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	kernel = np.ones((3,3), np.uint8)
	opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 2)
	
	sure_bg = cv2.dilate(opening, kernel, iterations=3)
	
	dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2,5)
	ret, sure_fg=cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
	
	sure_fg=np.uint8(sure_fg)
	unknown=cv2.subtract(sure_bg,sure_fg)
	
	ret, markers=cv2.connectedComponents(sure_fg)
	
	markers=markers+1
	
	markers[unknown==255]=0
	
	#markers=cv2.watershed(frame,markers)
	#frame[markers==-1]=[255,0,0]
	
	return thresh
	
	
def agt(frame):
	th1=cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
	cv2.THRESH_BINARY ,11,2)   
	return th1
	                                                                                                                                                                                                                                             
	
	
	
	
if __name__ == "__main__":
	while 1:
		frame = get_vid()
		depth = agt(get_depth())
		cv2.imshow('RGB image', frame)
		cv2.imshow('Depth image', depth)
		
		k = cv2.waitKey(5) & 0xFF
		if k==27:
			break
	cv2.destroyAllWindows()
