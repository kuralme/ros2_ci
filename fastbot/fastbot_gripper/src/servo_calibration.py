#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Setup
servo_pin = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 100)  # 100 Hz frequency

# Start with 0 duty cycle
pwm.start(0)

try:
    while True:
        # Get user input for duty cycle
        duty = float(input("Enter duty cycle (5-10 or 6-12, 0 to exit): "))
        if duty == 0:
            break
            
        # Apply duty cycle
        pwm.ChangeDutyCycle(duty)
        time.sleep(1)
        # Set to 0 to prevent holding current
        pwm.ChangeDutyCycle(0)
        
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()

