from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
camera.resolution = (320, 160)
camera.framerate = 10
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=(320, 160))

time.sleep(0.1)

CROP = range(60, 160)
RESIZE = (200, 66)


def process(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return cv2.resize(image[CROP], RESIZE)


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)  # clear buffer

    if key == ord("q"):
        break
