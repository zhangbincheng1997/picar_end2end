import RPi.GPIO as GPIO
import time

'''
Front Wheel control left and right.
====> 50HZ

0°      ---- 0.5ms   ---- 2.5%
45°     ---- 1.0ms   ---- 5.0%
90°     ---- 1.5ms   ---- 7.5%
135°    ---- 2.0ms   ---- 10.0%
180°    ---- 2.5ms   ---- 12.5%

Red     ---- +5V    ---- GPIO.2
Brown   ---- GND    ---- GPIO.6
Yellow  ---- SIG    ---- GPIO.12
'''

# Front Wheel
SIG = 12

# BOARD or BCM
GPIO.setmode(GPIO.BOARD)

GPIO.setup(SIG, GPIO.OUT)
car = GPIO.PWM(SIG, 50)  # 50HZ
car.start(0)

if __name__ == '__main__':
    try:
        while True:
            for i in range(5, 11, 1):
                car.ChangeDutyCycle(i)
                print(i)
                time.sleep(0.5)

            for i in range(10, 4, -1):
                car.ChangeDutyCycle(i)
                print(i)
                time.sleep(0.5)

    except KeyboardInterrupt:
        car.ChangeDutyCycle(7.5)
        time.sleep(1)
        car.stop()
        GPIO.cleanup()
        print('Exit...')
