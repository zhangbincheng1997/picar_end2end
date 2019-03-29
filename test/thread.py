import threading
import time


class Job(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        while self.__running.isSet():
            # True return
            # False block
            self.__flag.wait()
            print(time.time())
            time.sleep(1)

    def pause(self):
        self.__flag.clear()  # set False

    def resume(self):
        self.__flag.set()  # set True

    def stop(self):
        self.__flag.set()  # resume from pause
        self.__running.clear()


a = Job()
a.start()
time.sleep(3)
a.pause()
time.sleep(3)
a.resume()
time.sleep(3)
a.pause()
time.sleep(2)
a.stop()
