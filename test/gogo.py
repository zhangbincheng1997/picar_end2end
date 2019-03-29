import RPi.GPIO as GPIO
import time

'''
Rear Wheel control forward and backward.
====> 10kHZ-30kHz

SLP PWM DIR M+  M-  Status
H   H   H   H   L   Forward
H   H   L   L   H   Backward
H   L   X   L   L   Brake
L   X   X   X   X   Stop

SLP ---- GPIO.4(+5V)
GND ---- GPIO.9
DIR ---- GPIO.11
PWM ---- GPIO.13
'''

# Rear Wheel
SLP = 4
DIR = 11
PWM = 13

# BOARD or BCM
GPIO.setmode(GPIO.BOARD)

# GPIO.setup(SLP, GPIO.OUT) # +5V (The channel sent is invalid on a Raspberry Pi.)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PWM, GPIO.OUT)
car = GPIO.PWM(PWM, 10 * 1000)  # 10kHZ-30kHZ
car.start(0)

if __name__ == '__main__':
    try:
        while True:
            for i in range(10, 110, 10):
                GPIO.output(DIR, GPIO.HIGH)
                car.ChangeDutyCycle(i)
                print(i)
                time.sleep(0.5)

            for i in range(100, 0, -10):
                GPIO.output(DIR, GPIO.LOW)
                car.ChangeDutyCycle(i)
                print(i)
                time.sleep(0.5)

    except KeyboardInterrupt:
        car.ChangeDutyCycle(0)
        time.sleep(1)
        car.stop()
        GPIO.cleanup()
        print('Exit...')
