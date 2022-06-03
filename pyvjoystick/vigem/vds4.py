from . import _sdk
from .constants import (
    DS4_DPAD_DIRECTIONS,
    DS4_REPORT,
    DS4_REPORT_EX,
    DS4_REPORT_INIT,
    DS4_SET_DPAD,
)
from .device import VGamepad
from .utils import check_err


class VDS4Gamepad(VGamepad):
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__()

    def _target_alloc(self):
        return _sdk.vigem_target_ds4_alloc()

    def _get_default_report(self):
        rep = DS4_REPORT(
            bThumbLX=0,
            bThumbLY=0,
            bThumbRX=0,
            bThumbRY=0,
            wButtons=0,
            bSpecial=0,
            bTriggerL=0,
            bTriggerR=0)

        DS4_REPORT_INIT(rep)

        return rep

    def update(self):
        """
        Sends the current report (i.e. commands) to the virtual device
        """
        check_err(_sdk.vigem_target_ds4_update(
            self._bus_pointer, self._device_pointer, self._report))

    def update_extended_report(self, extended_report: DS4_REPORT_EX):
        """
        Enables using DS4_REPORT_EX instead of DS4_REPORT (advanced users only)
        If you don't know what this is about, you can safely ignore this function

        :param: a DS4_REPORT_EX
        """
        check_err(_sdk.vigem_target_ds4_update_ex(
            self._bus_pointer, self._device_pointer, extended_report))

    def press_special_button(self, special_button: int):
        """
        Presses a special button (no effect if already pressed)
        All possible buttons are in DS4_SPECIAL_BUTTONS

        :param: a DS4_SPECIAL_BUTTONS field, e.g. DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_TOUCHPAD
        """
        self._report.bSpecial = self._report.bSpecial | special_button

    def release_special_button(self, special_button: int):
        """
        Releases a special button (no effect if already released)
        All possible buttons are in DS4_SPECIAL_BUTTONS

        :param: a DS4_SPECIAL_BUTTONS field, e.g. DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_TOUCHPAD
        """
        self._report.bSpecial = self._report.bSpecial & ~special_button

    def left_trigger(self, value: int):
        """
        Sets the value of the left trigger

        :param: integer between 0 and 255 (0 = trigger released)
        """
        self._report.bTriggerL = value

    def right_trigger(self, value: int):
        """
        Sets the value of the right trigger

        :param: integer between 0 and 255 (0 = trigger released)
        """
        self._report.bTriggerR = value

    def left_joystick(self, x_value: float, y_value: float):
        """
        Sets the values of the X and Y axis for the left joystick

        :param: integer between -32768 and 32767 (0 = neutral position)
        """
        self._report.bThumbLX = x_value
        self._report.bThumbLY = y_value

    def right_joystick(self, x_value: float, y_value: float):
        """
        Sets the values of the X and Y axis for the right joystick

        :param: integer between -32768 and 32767 (0 = neutral position)
        """
        self._report.bThumbRX = x_value
        self._report.bThumbRY = y_value

    def left_joystick_float(self, x_value_float: float, y_value_float: float):
        """
        Sets the values of the X and Y axis for the left joystick

        :param: float between -1.0 and 1.0 (0 = neutral position)
        """
        self.left_joystick(128 + round(x_value_float * 127),
                           128 + round(y_value_float * 127))

    def right_joystick_float(self, x_value_float: float, y_value_float: float):
        """
        Sets the values of the X and Y axis for the right joystick

        :param: float between -1.0 and 1.0 (0 = neutral position)
        """
        self.right_joystick(128 + round(x_value_float * 127),
                            128 + round(y_value_float * 127))

    def directional_pad(self, direction: DS4_DPAD_DIRECTIONS):
        """
        Sets the direction of the directional pad (hat)
        All possible directions are in DS4_DPAD_DIRECTIONS

        :param: a DS4_DPAD_DIRECTIONS field, e.g. DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHWEST
        """
        DS4_SET_DPAD(self._report, direction)

    def _register_notification(self):
        check_err(_sdk.vigem_target_ds4_register_notification(
            self._bus_pointer, self._device_pointer, self._callback_func, None))

    def unregister_notification(self):
        """
        Unregisters a previously registered callback function.
        """
        _sdk.vigem_target_ds4_unregister_notification(self._device_pointer)
