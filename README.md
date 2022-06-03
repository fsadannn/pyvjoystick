# pyvjoystick

pyvjoystick is a set of python binding for different virtual devices. Currently [vJoy](https://sourceforge.net/projects/vjoystick/) and [ViGEm](https://github.com/ViGEm) are supported.

<a href='https://sourceforge.net/projects/vjoystick/'>vJoy</a>(on github from <a href='https://github.com/jshafer817/vJoy'>jshafer817</a> and <a href='https://github.com/njz3/vJoy/'>njz3</a>). The implementation of vjoy bindings are inspired on <a href="https://github.com/tidzo/pyvjoy">pyvjoy</a>'s package.


<a href='https://github.com/ViGEm'>ViGEm</a> bindings are inspired on <a href="https://github.com/yannbouteiller/vgamepad">vgamepad</a>'s package.

## Requirements

To be able to use vJoy device install vJoy from <a href='https://sourceforge.net/projects/vjoystick/'>sourceforge</a> or <a href='https://github.com/njz3/vJoy/'>github</a>. It is recommended to also install the vJoy Monitor and Configure vJoy programs. These should be an option during installation.

To be able to use ViGem device install [release](https://github.com/ViGEm/ViGEmBus). This package ships with a ViGemClient binaries.


### Installation

Simple! This package is installable by pip

`pip install pyvjoystick`


## Usage

### vJoy example

With this library you can easily set Axis and Button values on any vJoy device. Low-level bindings are provided in `pyvjoy._sdk`.

```python
from pyvjoystick import vjoy

# Pythonic API, item-at-a-time
j = vjoy.VJoyDevice(1)

# turn button number 15 on
j.set_button(15, 1)

# Notice the args are (buttonID,state) whereas vJoy's native API is the other way around.


# turn button 15 off again
j.set_button(15, 0)

# Set X axis to fully left
j.set_axis(vjoy.HID_USAGE.X, 0x1)

# Set X axis to fully right
j.set_axis(vjoy.HID_USAGE.X, 0x8000)

# Also implemented:

j.reset()
j.reset_buttons()
j.reset_povs()


# The 'efficient' method as described in vJoy's docs - set multiple values at once

print(j._data)
# >> > <pyvjoystick.vjoy._sdk._JOYSTICK_POSITION_V2 at 0x.... >


j._data.lButtons = 19  # buttons number 1,2 and 5 (1+2+16)
j._data.wAxisX = 0x2000
j._data.wAxisY = 0x7500

# send data to vJoy device
j.update()


# Lower-level API just wraps the functions in the DLL as thinly as possible, with some attempt to raise exceptions instead of return codes.
```

### XBox360 gamepad

The following python script creates a virtual XBox360 gamepad:

```python
from pyvjoystick import vigem as vg

gamepad = vg.VX360Gamepad()
```

As soon as the ```VX360Gamepad``` object is created, the virtual gamepad is connected to your system via the ViGEmBus driver, and will remain connected until the object is destroyed.

Buttons can be pressed and released through ```press_button``` and ```release_button```:

```python
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)  # press the A button
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)  # press the left hat button

gamepad.update()  # send the updated state to the computer

# (...) A and left hat are pressed...

gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)  # release the A button

gamepad.update()  # send the updated state to the computer

# (...) left hat is still pressed...
```

All available buttons are defined in ```XUSB_BUTTON```

To control the triggers (1 axis each) and the joysticks (2 axis each), two options are provided by the API.

It is possible to input raw integer values directly:
```python
gamepad.left_trigger(value=100)  # value between 0 and 255
gamepad.right_trigger(value=255)  # value between 0 and 255
gamepad.left_joystick(x_value=-10000, y_value=0)  # values between -32768 and 32767
gamepad.right_joystick(x_value=-32768, y_value=15000)  # values between -32768 and 32767

gamepad.update()
```

Or to input float values:
```python
gamepad.left_trigger_float(value_float=0.5)  # value between 0.0 and 1.0
gamepad.right_trigger_float(value_float=1.0)  # value between 0.0 and 1.0
gamepad.left_joystick_float(x_value_float=-0.5, y_value_float=0.0)  # values between -1.0 and 1.0
gamepad.right_joystick_float(x_value_float=-1.0, y_value_float=0.8)  # values between -1.0 and 1.0

gamepad.update()
```

Reset to default state:
```python
gamepad.reset()

gamepad.update()
```

### DualShock4 gamepad

Using a virtual DS4 gamepad is similar to X360:
```python
from pyvjoystick import vigem as vg

gamepad = vg.VDS4Gamepad()
```

Press and release buttons:
```python
gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)
gamepad.update()

# (...)

gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)
gamepad.update()
```

Available buttons are defined in ```DS4_BUTTONS```

Press and release special buttons:
```python
gamepad.press_special_button(special_button=vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS)
gamepad.update()

# (...)

gamepad.release_special_button(special_button=vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS)
gamepad.update()
```

Special buttons are defined in ```DS4_SPECIAL_BUTTONS```

Triggers and joysticks (integer values):
```python
gamepad.left_trigger(value=100)  # value between 0 and 255
gamepad.right_trigger(value=255)  # value between 0 and 255
gamepad.left_joystick(x_value=0, y_value=128)  # value between 0 and 255
gamepad.right_joystick(x_value=0, y_value=255)  # value between 0 and 255

gamepad.update()
```

Triggers and joysticks (float values):
```python
gamepad.left_trigger_float(value_float=0.5)  # value between 0.0 and 1.0
gamepad.right_trigger_float(value_float=1.0)  # value between 0.0 and 1.0
gamepad.left_joystick_float(x_value_float=-0.5, y_value_float=0.0)  # values between -1.0 and 1.0
gamepad.right_joystick_float(x_value_float=-1.0, y_value_float=0.8)  # values between -1.0 and 1.0

gamepad.update()
```

* **Note:** The Y axis on joysticks is inverted for consistency with the X360 API.

Directional pad (hat):
```python
gamepad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHWEST)
gamepad.update()
```

Directions for the directional pad are defined in ```DS4_DPAD_DIRECTIONS```

Reset to default state:
```python
gamepad.reset()

gamepad.update()
```