
import RPi.GPIO as GPIO
import time

#Pin definitions
motor_pin_a=18 #board pin 12 - left fwd
motor_pin_b=23 #board pin 16 - right fwd
motor_pin_c=24 #board pin 18 - left back
motor_pin_d=25 #board pin 22 - right back

def back():
	GPIO.output(motor_pin_a, GPIO.HIGH)
	GPIO.output(motor_pin_b, GPIO.HIGH)
	time.sleep(1.5)
	GPIO.output(motor_pin_a, GPIO.LOW)
	GPIO.output(motor_pin_b, GPIO.LOW)

def stop():
	GPIO.output(motor_pin_a, GPIO.LOW)
	GPIO.output(motor_pin_b, GPIO.LOW)
	GPIO.output(motor_pin_c, GPIO.LOW)
	GPIO.output(motor_pin_d, GPIO.LOW)

def fwd():
	GPIO.output(motor_pin_c, GPIO.HIGH)
	GPIO.output(motor_pin_d, GPIO.HIGH)
	time.sleep(1.6)
	GPIO.output(motor_pin_c, GPIO.LOW)
	GPIO.output(motor_pin_d, GPIO.LOW)

def left():
	GPIO.output(motor_pin_c, GPIO.HIGH)
	GPIO.output(motor_pin_b, GPIO.HIGH)
	time.sleep(1.6)
	GPIO.output(motor_pin_c, GPIO.LOW)
	GPIO.output(motor_pin_b, GPIO.LOW)
 
def right():
	GPIO.output(motor_pin_d,GPIO.HIGH)
	GPIO.output(motor_pin_a,GPIO.HIGH)
	time.sleep(1.7)
	GPIO.output(motor_pin_d,GPIO.LOW)
	GPIO.output(motor_pin_a,GPIO.LOW)

def main():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(motor_pin_a, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(motor_pin_b, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(motor_pin_c, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(motor_pin_d, GPIO.OUT, initial=GPIO.LOW)
	
	print('Starting')
	while True:
		i = input()
		if i == '1':
			stop()
		elif i == '2':
			fwd()
		elif i == '3':
			back()
		elif i == '4':
			left()
		elif i == '5':
			right()
		else:
			break
	print('Done')

def test():
#	while True:
#		print("Starting now!")	
#		GPIO.output(motor_pin_a, GPIO.HIGH)
#		GPIO.output(motor_pin_b, GPIO.HIGH)	

	curr_value_pin_a=GPIO.HIGH
	curr_value_pin_b=GPIO.HIGH
	A = 0
	try:
		while A<3:		
			time.sleep(2)
			GPIO.output(motor_pin_a, curr_value_pin_a)
			GPIO.output(motor_pin_b, curr_value_pin_b)
			
			curr_value_pin_a^=GPIO.HIGH
			curr_value_pin_b^=GPIO.HIGH
			curr_value_pin_a^=GPIO.LOW
			curr_value_pin_b^=GPIO.LOW
			A += 1
		GPIO.output(motor_pin_a, GPIO.LOW)
		GPIO.output(motor_pin_b, GPIO.LOW)
	finally:
		GPIO.cleanup()
		
		
if __name__=='__main__':
	main()
	

#		while True:
#			time.sleep(0.25)
#			if val >= 100:
#				incr=-incr
#			if val<=0:
#				incr=-incr
#			val+=incr
#			p.ChangeDutyCycle(val)
