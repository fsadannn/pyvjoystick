from enum import Enum

from pynput import keyboard

import my_pyvjoy

device = my_pyvjoy.VJoyDevice(1)


class Direction(Enum):
    Positive = 1
    Negative = -1


class Stick:
    __slots__ = ('axis', 'direction')

    def __init__(self, axis: my_pyvjoy.HID_USAGE, direction: Direction) -> None:
        self.axis = axis
        self.direction = direction


key_map = {
    'a': Stick(my_pyvjoy.HID_USAGE.RX, Direction.Negative),
    'd': Stick(my_pyvjoy.HID_USAGE.RX, Direction.Positive)
}


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))
        return

    data = key_map.get(key.char)


def on_release(key):
    print('{0} released'.format(key))

    if key == keyboard.Key.esc:
        # Stop listener
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    try:
        listener.join()
    except Exception as e:
        print('{0} was pressed'.format(e.args[0]))
