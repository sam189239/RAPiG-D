import RPi.GPIO as GPIO
import time

output_pin=33;

if output_pin is None:
	print("PWM not supported")
	
def main():

	
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)
	p=GPIO.PWM(output_pin, 50)
	val=25
	incr=25
	
	p.start(val)
	
	print("Running!") 
	try:
		while True:
			time.sleep(2)
			if val >= 100:
				incr=-incr
			if val<=0:
				incr=-incr
			val+=incr
			print(val)
			p.ChangeDutyCycle(val)
			#GPIO.output(output_pin, val)
			print("Duty cycle changed!")
			
	finally:
		p.stop()
		GPIO.cleanup()
		
		
if __name__=='__main__':
	main()
