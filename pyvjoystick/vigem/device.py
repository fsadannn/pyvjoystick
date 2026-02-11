from abc import ABC, abstractmethod
from ctypes import CFUNCTYPE, Structure, c_ubyte, c_void_p
from inspect import signature

from . import _sdk
from .constants import VIGEM_TARGET_TYPE
from .exceptions import ViGemBusConnectionError
from .utils import dummy_callback
from .vbus import VBus


class VGamepad(ABC):
    __slots__ = ('_bus_pointer', '_device_pointer',
                 '_FUNC_TYPE', '_callback_func', '_report')

    def __init__(self) -> None:
        self._bus_pointer = VBus.getVBus().bus_pointer
        self._device_pointer = self._target_alloc()
        self._FUNC_TYPE = CFUNCTYPE(
            None, c_void_p, c_void_p, c_ubyte, c_ubyte, c_ubyte, c_void_p)
        self._callback_func = None

        _sdk.vigem_target_add(self._bus_pointer, self._device_pointer)

        if not _sdk.vigem_target_is_attached(self._device_pointer):
            raise ViGemBusConnectionError(
                "The virtual device could not connect to ViGEmBus.")

        self._report = self._get_default_report()
        self.update()

    def __del__(self):
        _sdk.vigem_target_remove(self._bus_pointer, self._device_pointer)
        _sdk.vigem_target_free(self._device_pointer)

    @abstractmethod
    def _target_alloc(self):
        """
        :return: the pointer to an allocated ViGEm device (e.g. _sdk.vigem_target_x360_alloc())
        """
        raise NotImplementedError

    @abstractmethod
    def _get_default_report(self) -> Structure:
        """
        :return: the default structure used to update the status of the device
        """
        raise NotImplementedError

    @abstractmethod
    def update(self):
        """
        Sends the current report (i.e. commands) to the virtual device
        """
        raise NotImplementedError

    def update_extended_report(self, extended_report: Structure):
        """
        Enables using DS4_REPORT_EX instead of DS4_REPORT (advanced users only)
        If you don't know what this is about, you can safely ignore this function

        Not all device implement this api

        :param: a DS4_REPORT_EX
        """
        raise NotImplementedError

    def reset(self):
        """
        Resets the report to the default state
        """
        self._report = self._get_default_report()

    def get_vid(self) -> int:
        """
        :return: the vendor ID of the virtual device
        """
        return _sdk.vigem_target_get_vid(self._device_pointer).value

    def get_pid(self) -> int:
        """
        :return: the product ID of the virtual device
        """
        return _sdk.vigem_target_get_pid(self._device_pointer).value

    def set_vid(self, vid):
        """
        :param: the new vendor ID of the virtual device
        """
        _sdk.vigem_target_set_vid(self._device_pointer, vid)

    def set_pid(self, pid):
        """
        :param: the new product ID of the virtual device
        """
        _sdk.vigem_target_get_pid(self._device_pointer, pid)

    def get_index(self) -> int:
        """
        :return: the internally used index of the target device
        """
        return _sdk.vigem_target_get_index(self._device_pointer).value

    def get_type(self) -> VIGEM_TARGET_TYPE:
        """
        :return: the type of the object (e.g. VIGEM_TARGET_TYPE.Xbox360Wired)
        """
        return _sdk.vigem_target_get_type(self._device_pointer)

    def press_button(self, button: int):
        """
        Presses a button (no effect if already pressed)
        :param: an int representing the button id, e.g. XUSB_BUTTON.XUSB_GAMEPAD_X or DS4_BUTTONS.DS4_BUTTON_TRIANGLE
        """
        self._report.wButtons = self._report.wButtons | button

    def release_button(self, button: int):
        """
        Releases a button (no effect if already released)
        :param: an int representing the button id, e.g. XUSB_BUTTON.XUSB_GAMEPAD_X or DS4_BUTTONS.DS4_BUTTON_TRIANGLE
        """
        self._report.wButtons = self._report.wButtons & ~button

    def press_special_button(self, special_button: int):
        """
        Presses a special button (no effect if already pressed)
        Not all device implement this buttons

        :param: an of the button id, e.g. DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_TOUCHPAD
        """
        raise NotImplementedError

    def release_special_button(self, special_button: int):
        """
        Releases a special button (no effect if already released)
        Not all device implement this buttons

        :param: an of the button id, e.g. DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_TOUCHPAD
        """
        raise NotImplementedError

    @abstractmethod
    def left_trigger(self, value: int):
        """
        Sets the value of the left trigger

        :param: integer between 0 and 255 (0 = trigger released)
        """
        raise NotImplementedError

    @abstractmethod
    def right_trigger(self, value: int):
        """
        Sets the value of the right trigger

        :param: integer between 0 and 255 (0 = trigger released)
        """
        raise NotImplementedError

    def left_trigger_float(self, value_float):
        """
        Sets the value of the left trigger

        :param: float between 0.0 and 1.0 (0.0 = trigger released)
        """
        self.left_trigger(round(value_float * 255))

    def right_trigger_float(self, value_float):
        """
        Sets the value of the right trigger

        :param: float between 0.0 and 1.0 (0.0 = trigger released)
        """
        self.right_trigger(round(value_float * 255))

    @abstractmethod
    def left_joystick(self, x_value: int, y_value: int):
        """
        Sets the values of the X and Y axis for the left joystick

        :param: integer, value range depend on the specific api
        """
        raise NotImplementedError

    @abstractmethod
    def right_joystick(self, x_value: int, y_value: int):
        """
        Sets the values of the X and Y axis for the right joystick

        :param: integer, value range depend on the specific api
        """
        raise NotImplementedError

    @abstractmethod
    def left_joystick_float(self, x_value_float: float, y_value_float: float):
        """
        Sets the values of the X and Y axis for the left joystick

        :param: float between -1.0 and 1.0 (0 = neutral position)
        """
        raise NotImplementedError

    @abstractmethod
    def right_joystick_float(self, x_value_float: float, y_value_float: float):
        """
        Sets the values of the X and Y axis for the right joystick

        :param: float between -1.0 and 1.0 (0 = neutral position)
        """
        raise NotImplementedError

    def directional_pad(self, direction: int):
        """
        Sets the direction of the directional pad (hat)
        All possible directions are in DS4_DPAD_DIRECTIONS
        Not all device implement this api

        :param: a DS4_DPAD_DIRECTIONS field, e.g. DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHWEST
        """
        raise NotImplementedError

    @abstractmethod
    def _register_notification(self):
        """
        Registers a callback function that can handle force feedback, leds, etc.

        call the properly api function to register `self.__callback_func`
        """
        raise NotImplementedError

    def register_notification(self, callback_function):
        """
        Registers a callback function that can handle force feedback, leds, etc.

        :param: a function of the form: my_func(client, target, large_motor, small_motor, led_number, user_data)
        """
        if not signature(callback_function) == signature(dummy_callback):
            raise TypeError(
                f"Needed callback function signature: {signature(dummy_callback)}, but got: {signature(callback_function)}")

        # keep its reference, otherwise the program will crash when a callback is made.
        self._callback_func = self._FUNC_TYPE(callback_function)
        self._register_notification()

    @abstractmethod
    def unregister_notification(self):
        """
        Unregisters a previously registered callback function.
        """
        raise NotImplementedError
