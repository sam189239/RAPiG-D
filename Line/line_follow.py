import RPi.GPIO as GPIO
import time


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

def main():
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

  


if __name__ == '__main__':
    main()
