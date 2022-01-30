import RPi.GPIO as GPIO
import time

#Pin definitions
motor_pin_a=18 #board pin 12
motor_pin_b=23 #board pin 16

def main():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(motor_pin_a, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(motor_pin_b, GPIO.OUT, initial=GPIO.LOW)

#	while True:
#		print("Starting now!")	
#		GPIO.output(motor_pin_a, GPIO.HIGH)
#		GPIO.output(motor_pin_b, GPIO.HIGH)	

	curr_value_pin_a=GPIO.HIGH
	curr_value_pin_b=GPIO.HIGH
	try:
		while True:		
			time.sleep(2)
			GPIO.output(motor_pin_a, curr_value_pin_a)
			GPIO.output(motor_pin_b, curr_value_pin_b)
			
			curr_value_pin_a^=GPIO.HIGH
			curr_value_pin_b^=GPIO.HIGH
			curr_value_pin_a^=GPIO.LOW
			curr_value_pin_b^=GPIO.LOW
			
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
