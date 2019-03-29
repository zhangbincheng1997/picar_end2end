import struct
import time

'''
https://www.kernel.org/doc/Documentation/input/joystick-api.txt
struct js_event {
    __u32 time;     /* event timestamp in milliseconds */
    __s16 value;    /* value */
    __u8 type;      /* event type */
    __u8 number;    /* axis/button number */
};
'''

JS_EVENT_BUTTON = 0x01  # button pressed/released
JS_EVENT_AXIS = 0x02  # joystick moved

BUTTON_A = 0
BUTTON_B = 1
BUTTON_X = 3
BUTTON_Y = 4
BUTTON_LB = 6  # L1按键
BUTTON_RB = 7  # R1按键
BUTTON_MENU = 11
BUTTON_LO = 13  # 左摇杆按键
BUTTON_RO = 14  # 右摇杆按键

AXIS_LX = 0  # 左摇杆X轴
AXIS_LY = 1  # 左摇杆Y轴
AXIS_RX = 2  # 右摇杆X轴
AXIS_RY = 3  # 右摇杆Y轴
AXIS_LT = 4  # L2按键
AXIS_RT = 5  # R2按键
AXIS_XX = 6  # 方向键X轴
AXIS_YY = 7  # 方向键Y轴


# MIN_NUMBER = -32767
# MAX_NUMBER = +32767

class Map:
    time = 0

    a = 0
    b = 0
    x = 0
    y = 0
    lb = 0
    rb = 0
    menu = 0
    lo = 0
    ro = 0

    lx = 0
    ly = 0
    rx = 0
    ry = 0
    lt = -32767
    rt = -32767
    xx = 0
    yy = 0


class Joystick:
    def __init__(self, dev_path='/dev/input/js0'):
        self.EVENT_SIZE = struct.calcsize('IhBB')
        self.dev = open(dev_path, 'rb')
        self.map = Map()

    def run(self):
        event = self.dev.read(self.EVENT_SIZE)
        (time, value, type, number) = struct.unpack('IhBB', event)
        self.map.time = time

        if type & JS_EVENT_BUTTON:
            if number == BUTTON_A:
                self.map.a = value
            if number == BUTTON_B:
                self.map.b = value
            if number == BUTTON_X:
                self.map.x = value
            if number == BUTTON_Y:
                self.map.y = value
            if number == BUTTON_LB:  # L1按键
                self.map.lb = value
            if number == BUTTON_RB:  # R1按键
                self.map.rb = value
            if number == BUTTON_MENU:
                self.map.menu = value
            if number == BUTTON_LO:  # 左摇杆按键
                self.map.lo = value
            if number == BUTTON_RO:  # 右摇杆按键
                self.map.ro = value

        if type == JS_EVENT_AXIS:
            if number == AXIS_LX:  # 左摇杆X轴
                self.map.lx = value
            if number == AXIS_LY:  # 左摇杆Y轴
                self.map.ly = value
            if number == AXIS_RX:  # 右摇杆X轴
                self.map.rx = value
            if number == AXIS_RY:  # 右摇杆Y轴
                self.map.ry = value
            if number == AXIS_LT:  # L1按键
                self.map.lt = value
            if number == AXIS_RT:  # L2按键
                self.map.rt = value
            if number == AXIS_XX:  # 方向键X轴
                self.map.xx = value
            if number == AXIS_YY:  # 方向键Y轴
                self.map.yy = value

        return self.map

    def stop(self):
        if self.dev:
            self.dev.close()


if __name__ == '__main__':
    js = Joystick()

    try:
        while True:
            map = js.run()
            print("Time:%8d"
                  " A:%d B:%d X:%d Y:%d LB:%d RB:%d MENU:%d LO:%d RO:%d"
                  " LX:%-6d LY:%-6d RX:%-6d RY:%-6d LT:%-6d RT:%-6d XX:%-6d YY:%-6d" %
                  (map.time,
                   map.a, map.b, map.x, map.y, map.lb, map.rb, map.menu, map.lo, map.ro,
                   map.lx, map.ly, map.rx, map.ry, map.lt, map.rt, map.xx, map.yy), end='\r')

    except KeyboardInterrupt:
        print('Exit...')
        js.stop()
        exit()
