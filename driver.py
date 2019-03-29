from car import Car
from model import MyModel

from picamera.array import PiRGBArray
from picamera import PiCamera

import time
import cv2
import numpy as np

MAX = 32767  # Joystick
CROP = range(60, 160)
SIZE = (320, 160)
RESIZE = (200, 66)

model = MyModel()
model.load_weights('train/model/model.h5')
model._make_predict_function()

camera = PiCamera()
camera.resolution = SIZE
camera.framerate = 10
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=SIZE)


def process(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return cv2.resize(image[CROP], RESIZE)


if __name__ == '__main__':
    car = Car()
    car.gogo(-2000)  # move

    try:
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            image = process(image)
            image = np.expand_dims(image, axis=0)
            preds = model.predict(image)

            x = preds * MAX
            print('pred: %f' % x)
            car.turn(x)

            rawCapture.truncate(0)  # clear buffer
    except KeyboardInterrupt:
        car.stop()
        time.sleep(1)
        print('Exit...')
