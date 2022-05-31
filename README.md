# pyvjoystick

pyvjoystick is a set of python binding for <a href='https://sourceforge.net/projects/vjoystick/'>vJoy</a>(on github from <a href='https://github.com/jshafer817/vJoy'>jshafer817</a> and <a href='https://github.com/njz3/vJoy/'>njz3</a>). This repository is based off <a href="https://github.com/tidzo/pyvjoy">tidzo</a>'s package.


I will extend the support for others vJoysticks like ScpVBus.
### Requirements

Install vJoy from <a href='https://sourceforge.net/projects/vjoystick/'>sourceforge</a> or <a href='https://github.com/njz3/vJoy/'>github</a>. It is recommended to also install the vJoy Monitor and Configure vJoy programs. These should be an option during installation.


### Installation

Simple! This package is installable by pip

`pip install pyvjoystick`


### Usage

With this library you can easily set Axis and Button values on any vJoy device. Low-level bindings are provided in `pyvjoy._sdk`.

```python
import pyvjoy

#Pythonic API, item-at-a-time
j = pyvjoy.VJoyDevice(1)

#turn button number 15 on
j.set_button(15,1)

#Notice the args are (buttonID,state) whereas vJoy's native API is the other way around.


#turn button 15 off again
j.set_button(15,0)

#Set X axis to fully left
j.set_axis(pyvjoy.HID_USAGE_X, 0x1)

#Set X axis to fully right
j.set_axis(pyvjoy.HID_USAGE_X, 0x8000)

#Also implemented:

j.reset()
j.reset_buttons()
j.reset_povs()


#The 'efficient' method as described in vJoy's docs - set multiple values at once

j.data
>>> <pyvjoy._sdk._JOYSTICK_POSITION_V2 at 0x....>


j.data.lButtons = 19 # buttons number 1,2 and 5 (1+2+16)
j.data.wAxisX = 0x2000 
j.data.wAxisY= 0x7500

#send data to vJoy device
j.update()


#Lower-level API just wraps the functions in the DLL as thinly as possible, with some attempt to raise exceptions instead of return codes.
```