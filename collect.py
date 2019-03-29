from joystick import Joystick
from car import Car

from picamera.array import PiRGBArray
from picamera import PiCamera

import threading
import time
import cv2

map = None


class Camera(threading.Thread):
    global map

    def __init__(self, *args, **kwargs):
        super(Camera, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()  # resume/pause thread event
        self.__running = threading.Event()  # start/stop thread event

        self.number = 0
        self.camera = PiCamera()
        self.camera.resolution = (320, 160)
        self.camera.framerate = 10
        self.camera.rotation = 180
        self.rawCapture = PiRGBArray(self.camera, size=(320, 160))

        self.map = map

        time.sleep(1)
        print('thread ok!!!')

    def run(self):
        self.__running.set()  # set True

        with open('content.csv', 'w') as f:
            f.write('image,steer\n')
            for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                if self.__running.isSet():
                    # True return
                    # False block
                    self.__flag.wait()
                    if not self.__running.isSet():  # double check
                        break

                    self.number += 1
                    path = 'IMG/%06d.jpg' % self.number
                    line = '%s,%f' % (path, map.rx)
                    cv2.imwrite(path, frame.array)
                    f.write(line + '\n')
                    print(line)

                self.rawCapture.truncate(0)  # clear buffer

    def pause(self):
        self.__flag.clear()  # set False

    def resume(self):
        self.__flag.set()  # set True

    def stop(self):
        self.__flag.set()  # resume from pause
        self.__running.clear()

    def running(self):
        return self.__flag.isSet()


if __name__ == '__main__':
    js = Joystick()
    car = Car()
    camera = Camera()
    camera.start()

    try:
        while True:
            map = js.run()

            x = map.rx
            car.turn(x)

            # y = map.ly
            # car.turn(y)

            if map.menu == 1:
                if camera.running():
                    car.gogo(0)
                    camera.pause()
                    print('camera pause')
                else:
                    car.gogo(-2000)
                    camera.resume()
                    print('camera resume')


    except KeyboardInterrupt:
        js.stop()
        car.stop()
        camera.stop()
        time.sleep(1)
        print('Exit...')
