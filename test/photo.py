import picamera
import time

camera = picamera.PiCamera()
camera.resolution = (320, 160)
camera.rotation = 180

camera.start_preview()
time.sleep(5)
camera.capture('photo.jpg')
camera.stop_preview()
