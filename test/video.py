import picamera
import time

camera = picamera.PiCamera()
camera.resolution = (320, 160)
camera.rotation = 180

camera.start_preview()
camera.start_recording('video.h264')
time.sleep(5)
camera.stop_recording()
camera.stop_preview()

# sudo apt-get install -y gpac
# MP4Box -fps 30 -add video.h264 video.mp4
