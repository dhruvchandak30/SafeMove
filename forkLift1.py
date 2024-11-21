import socket
import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Ultrasonic Sensor Pins
TRIG_PIN = 23  # GPIO pin for TRIG
ECHO_PIN = 24  # GPIO pin for ECHO

# Motor Pins
motor_in1 = 22  # GPIO 22 (pin 15)
motor_in2 = 23  # GPIO 23 (pin 16)
motor_in3 = 25  # GPIO 25 (pin 22)
motor_in4 = 24  # GPIO 24 (pin 18)

# Setup pins
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(motor_in1, GPIO.OUT)
GPIO.setup(motor_in2, GPIO.OUT)
GPIO.setup(motor_in3, GPIO.OUT)
GPIO.setup(motor_in4, GPIO.OUT)

GPIO.output(TRIG_PIN, False)
GPIO.output(motor_in1, GPIO.LOW)
GPIO.output(motor_in2, GPIO.LOW)
GPIO.output(motor_in3, GPIO.LOW)
GPIO.output(motor_in4, GPIO.LOW)

# Socket setup
HOST = '172.22.58.41'  # First forklift's IP address
PORT = 65438


def measure_distance():
    # Ensure the TRIG pin is low
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)  # Allow sensor to settle

    # Trigger the sensor
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)  # TRIG high for 10 microseconds
    GPIO.output(TRIG_PIN, False)

    # Wait for ECHO to go high (start time)
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    # Wait for ECHO to go low (end time)
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Calculate the pulse duration
    pulse_duration = pulse_end - pulse_start

    # Convert pulse duration to distance in cm
    distance = pulse_duration * 17150  # Sound speed at 34300 cm/s, divided by 2
    return round(distance, 2)


def move_forward():
    GPIO.output(motor_in1, GPIO.HIGH)
    GPIO.output(motor_in2, GPIO.LOW)
    GPIO.output(motor_in3, GPIO.HIGH)
    GPIO.output(motor_in4, GPIO.LOW)
    print("Moving forward")


def stop_vehicle():
    GPIO.output(motor_in1, GPIO.LOW)
    GPIO.output(motor_in2, GPIO.LOW)
    GPIO.output(motor_in3, GPIO.LOW)
    GPIO.output(motor_in4, GPIO.LOW)
    print("Vehicle stopped")


try:
    # Establish socket connection first
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server ready, waiting for connection from second forklift...")

        conn, addr = s.accept()
        print(f"Connected by {addr}")

        # Start vehicle movement after connection
        while True:
            move_forward()
            time.sleep(0.1)  # Short delay for consistent movement
            dist = measure_distance()
            print(f"Distance: {dist} cm")

            if dist < 25:
                print("Obstacle detected! Sending STOP signal...")
                conn.sendall(b'STOP')
                stop_vehicle()
                break

except KeyboardInterrupt:
    print("Shutting down...")

finally:
    GPIO.cleanup()
