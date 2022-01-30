import pylibfreenect2 as f2
import cv2
import numpy as np

@attr('require_device')
def test_openDefaultDevice():
	fn = f2.Freenect2()
	print(fn.enumerateDevices())
	
if __name__ == "__main__":
	'''
	while 1:
		frame = get_vid()
		depth = get_depth()
		cv2.imshow('RGB image', frame)
		cv2.imshow('Depth image', depth)
		
		k = cv2.waitKey(5) & 0xFF
		if k==27:
			break
	cv2.destroyAllWindows()
	'''
	test_openDefaultDevice()
	
