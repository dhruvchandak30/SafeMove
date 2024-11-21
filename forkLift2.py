import socket
import RPi.GPIO as GPIO
import time
from time import sleep

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor pins based on your circuit diagram
motor_in1 = 22  # GPIO 22 (pin 15)
motor_in2 = 23  # GPIO 23 (pin 16)
motor_in3 = 25  # GPIO 25 (pin 22)
motor_in4 = 24  # GPIO 24 (pin 18)

# Setup motor pins
GPIO.setup(motor_in1, GPIO.OUT)
GPIO.setup(motor_in2, GPIO.OUT)
GPIO.setup(motor_in3, GPIO.OUT)
GPIO.setup(motor_in4, GPIO.OUT)

def move_forward():
    GPIO.output(motor_in1, GPIO.HIGH)
    GPIO.output(motor_in2, GPIO.LOW)
    GPIO.output(motor_in3, GPIO.HIGH)
    GPIO.output(motor_in4, GPIO.LOW)
    print("Moving forward")

def stop_motors():
    GPIO.output(motor_in1, GPIO.LOW)
    GPIO.output(motor_in2, GPIO.LOW)
    GPIO.output(motor_in3, GPIO.LOW)
    GPIO.output(motor_in4, GPIO.LOW)
    print("Stopping")

buzzer=18
GPIO.setup(buzzer,GPIO.OUT)
GPIO.output(buzzer, GPIO.LOW)

def beep_buzzer():
	GPIO.output(buzzer,GPIO.HIGH)
	print("Beep")
	time.sleep(2)
	GPIO.output(buzzer,GPIO.LOW)
	print("NO Beep")
	
HOST = '172.22.58.41'
PORT = 65438

try:
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
		s.connect((HOST,PORT))
		print("Connected to the 1st Forklift.")
		while True:
			move_forward()
			data = s.recv(1024)
			print(data)
			if data == b'STOP':
				stop_motors()
				break
			else: GPIO.output(buzzer, GPIO.LOW)
		beep_buzzer()
except Exception as e:
	print(f"An error occured: {e}")
finally:
	GPIO.cleanup()
