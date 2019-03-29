from joystick import Joystick
import RPi.GPIO as GPIO
import time

# Joystick
MIN_NUM = -32767
MAX_NUM = +32767


class Car():
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

    --------------------

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

    def __init__(self):
        # Front Wheel
        self.SIG = 12
        self.MIN_ANGLE = 5
        self.MAX_ANGLE = 10
        self.IDLE_ANGLE = 7.5
        self.x = 0

        # Rear Wheel
        self.SLP = 4
        self.DIR = 11
        self.PWM = 13
        self.MIN_SPEED = 0
        self.MAX_SPEED = 100
        self.IDLE_SPEED = 0
        self.y = 0

        # BOARD or BCM
        GPIO.setmode(GPIO.BOARD)

        # Front Wheel
        GPIO.setup(self.SIG, GPIO.OUT)
        self.car1 = GPIO.PWM(self.SIG, 50)  # 50HZ
        self.car1.start(0)

        # Rear Wheel
        GPIO.setup(self.SIG, GPIO.OUT)
        # GPIO.setup(SLP, GPIO.OUT)  # +5V (The channel sent is invalid on a Raspberry Pi.)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.PWM, GPIO.OUT)
        self.car2 = GPIO.PWM(self.PWM, 10 * 1000)  # 10kHZ-30kHZ
        self.car2.start(0)

    def turn(self, x=0):
        self.x = x
        angle = (x / MAX_NUM) * 90 + 90
        duty = (angle / 180) * (self.MAX_ANGLE - self.MIN_ANGLE) + self.MIN_ANGLE
        self.car1.ChangeDutyCycle(duty)

    def gogo(self, y=0):
        self.y = y
        duty = (y / MAX_NUM) * (self.MAX_SPEED - self.MIN_SPEED) + self.MIN_SPEED
        if y < 0:  # forward
            GPIO.output(self.DIR, GPIO.HIGH)
            self.car2.ChangeDutyCycle(-duty)
        if y > 0:  # backward
            GPIO.output(self.DIR, GPIO.LOW)
            self.car2.ChangeDutyCycle(+duty)
        if y == 0:  # brake
            self.car2.ChangeDutyCycle(0)

    def stop(self):
        self.car1.ChangeDutyCycle(self.IDLE_ANGLE)
        self.car2.ChangeDutyCycle(self.IDLE_SPEED)
        self.car1.stop()
        self.car2.stop()
        GPIO.cleanup()


if __name__ == '__main__':
    js = Joystick()
    car = Car()

    try:
        while True:
            map = js.run()

            x = map.rx
            car.turn(x)

            y = map.ly
            car.gogo(y)

            print('x = %f, y = %f' % (x, y))

    except KeyboardInterrupt:
        js.stop()
        car.stop()
        time.sleep(1)
        print('Exit...')
