import RPi.GPIO as GPIO
import time

board_pins = [7, 8, 10, 11, 13, 15, 19, 21, 23, 24]
ir_in = [4, 17, 27, 22, 10, 9, 11, 8]
#sensor = 13
#main = 3

def test():
    GPIO.setmode(GPIO.BCM)
    for a in range(len(ir_in)):
        GPIO.setup(ir_in[a], GPIO.IN)


    print("IR Sensor Ready.....")
    print(" ")
    n=0
    try: 
	    #GPIO.output(main, GPIO.HIGH)
        while True:
		#if GPIO.input(ir_in):
		 #   print("Object Detected")
		  #  while GPIO.input(sensor):
		   #     time.sleep(1)
		    #    print(n)
		     #   n+=1
		#else:
		 #   print("Off")
		  #  time.sleep(1)
            for a in range(len(ir_in)):
                print(GPIO.input(ir_in[a]), end = " ")
            print(" ")    

    except KeyboardInterrupt:
        GPIO.cleanup()
    


if __name__ == '__main__':
    test()
