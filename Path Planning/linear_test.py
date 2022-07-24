import sys
sys.path.append("../")
import RPi.GPIO as GPIO
import time
import freenect
import cv2
from Kinect.demo import frame_convert2
import numpy as np
import time
import datetime as dt

alert_thresh = 0.1
threshold = 150
current_depth = 450
height = 480
width = 640
roi_val = 0.2

ROI = [(int(width * roi_val), int(height * roi_val)), (int(width * (1-roi_val)), int(height * (1-roi_val)))]

board_pins = [7, 8, 10, 11, 13, 15, 19, 21, 23, 24]
ir_in = [4, 17, 27, 22, 10, 9, 11, 8]


motor_pin_a=18 #board pin 12 - left back
motor_pin_b=23 #board pin 16 - right back
motor_pin_c=24 #board pin 18 - left fwd
motor_pin_d=25 #board pin 22 - right fwd


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(motor_pin_a, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(motor_pin_b, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(motor_pin_c, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(motor_pin_d, GPIO.OUT, initial=GPIO.LOW)

for a in range(len(ir_in)):
    GPIO.setup(ir_in[a], GPIO.IN)
 
def stop():
    GPIO.output(motor_pin_a, GPIO.LOW)
    GPIO.output(motor_pin_b, GPIO.LOW)
    GPIO.output(motor_pin_c, GPIO.LOW)
    GPIO.output(motor_pin_d, GPIO.LOW)
    
def fwd():
    stop()

    GPIO.output(motor_pin_d, GPIO.HIGH)
    GPIO.output(motor_pin_c, GPIO.HIGH)
    GPIO.output(motor_pin_a, GPIO.LOW)
    GPIO.output(motor_pin_b, GPIO.LOW)
    

def back():
    stop()
    GPIO.output(motor_pin_a, GPIO.HIGH)
    GPIO.output(motor_pin_b, GPIO.HIGH)
    GPIO.output(motor_pin_c, GPIO.LOW)
    GPIO.output(motor_pin_d, GPIO.LOW)
    
def left():
    stop()
    GPIO.output(motor_pin_c, GPIO.HIGH)
    GPIO.output(motor_pin_b, GPIO.HIGH)
    GPIO.output(motor_pin_a, GPIO.LOW)
    GPIO.output(motor_pin_d, GPIO.LOW)
    
def right():
    stop()
    GPIO.output(motor_pin_d,GPIO.HIGH)
    GPIO.output(motor_pin_a,GPIO.HIGH)	
    GPIO.output(motor_pin_b,GPIO.LOW)
    GPIO.output(motor_pin_c,GPIO.LOW)
    

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
    if is_obj: 
        color = (0, 0, 255)
        print('Object')
        try:
        	send_to_flask(True)
        except Exception as e:
        	pass
        time.sleep(1)
    else: 
        color = (0, 255, 0)
        try:
        	send_to_flask(False)
        except Exception as e:
        	pass
    
    frame = cv2.rectangle(depth, ROI[0], ROI[1], color, 1)
    
    
    cv2.imshow('Depth', frame)


def test():
    print("IR Sensor Ready.....")
    print(" ")
    n=0
    try: 
        while True:
            for a in range(len(ir_in)):
                print(GPIO.input(ir_in[a]), end = " ")
            print(" ")    

    except KeyboardInterrupt:
        GPIO.cleanup()

def sum(s):
    ans = 0
    for a in s:
        ans = ans + a
    return ans

def line_follow():
    start = False
    a = input()
    if a.lower() == 'y':
        start = True
    try: 
        while start:
            s = []
            for a in range(len(ir_in)):
                #print(GPIO.input(ir_in[a]), end = " ")
                s.append(GPIO.input(ir_in[a]))
            #time.sleep(0.3)
            # if no black line
            if sum(s) == 0 or sum(s) == 8:
               stop()
               
            
            elif (s[0]+s[1]+s[2]+s[3]) > (s[4]+s[5]+s[6]+s[7]):
                right()
            
            elif (s[0]+s[1]+s[2]+s[3]) < (s[4]+s[5]+s[6]+s[7]):
                left()
                
            else:
                fwd()
                    
              

    except KeyboardInterrupt:
        GPIO.cleanup()

def move_one_f_line():
    start = dt.datetime.now()
    end = dt.datetime.now() + dt.timedelta(seconds = 1.5)
    while dt.datetime.now()<end:
        s = []
        for a in range(len(ir_in)):
            #print(GPIO.input(ir_in[a]), end = " ")
            s.append(GPIO.input(ir_in[a]))
        #time.sleep(0.3)
        # if no black line
        if sum(s) == 0:
           stop()    
                     
        elif (s[0]+s[1]+s[2]+s[3]) > (s[4]+s[5]+s[6]+s[7]):
            right()
           
        elif (s[0]+s[1]+s[2]+s[3]) < (s[4]+s[5]+s[6]+s[7]):
            left()
                
        else:
            fwd()
    stop()
    time.sleep(5)

def move_one_f():
    fwd()
    time.sleep(1.32)
    stop()
    time.sleep(1)

def move_one_b():
    back()
    time.sleep(1.32)
    stop()
    time.sleep(1)
    
def is_obstacle():
    global threshold
    global current_depth
    print("checking if obstacle... ")
    depth, timestamp = freenect.sync_get_depth()
    depth = 255 * np.logical_and(depth >= 0,
                                 depth <= current_depth + threshold)
    depth = depth.astype(np.uint8)
    depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB) 
    return check_if_object(depth)


def main():
    
    map = ["start"]
    start = False
    a = input("Press y to start: ")
    if a.lower() == 'y':
        start = True
    
    try:
        print("Starting...")
        while start:
           
            if is_obstacle():
                map.append("Obstacle")
                print("Obstacle detected")
                break
            else:
                map.append("Empty")
                print("Moving forward")
                move_one_f_line()
                continue
        print("Completed")
        print(map)
    
    except KeyboardInterrupt:
        GPIO.cleanup()
    
    


if __name__ == '__main__':
    main()
