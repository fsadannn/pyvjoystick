from . import _sdk
from .constants import XUSB_REPORT
from .device import VGamepad
from .utils import check_err


class VX360Gamepad(VGamepad):
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__()

    def _target_alloc(self):
        return _sdk.vigem_target_x360_alloc()

    def _get_default_report(self):
        return XUSB_REPORT(
            wButtons=0,
            bLeftTrigger=0,
            bRightTrigger=0,
            sThumbLX=0,
            sThumbLY=0,
            sThumbRX=0,
            sThumbRY=0)

    def update(self):
        """
        Sends the current report (i.e. commands) to the virtual device
        """
        check_err(_sdk.vigem_target_x360_update(
            self._bus_pointer, self._device_pointer, self._report))

    def left_trigger(self, value: int):
        """
        Sets the value of the left trigger

        :param: integer between 0 and 255 (0 = trigger released)
        """
        self._report.bLeftTrigger = value

    def right_trigger(self, value: int):
        """
        Sets the value of the right trigger

        :param: integer between 0 and 255 (0 = trigger released)
        """
        self._report.bRightTrigger = value

    def left_joystick(self, x_value: float, y_value: float):
        """
        Sets the values of the X and Y axis for the left joystick

        :param: integer between -32768 and 32767 (0 = neutral position)
        """
        self._report.sThumbLX = x_value
        self._report.sThumbLY = y_value

    def right_joystick(self, x_value: float, y_value: float):
        """
        Sets the values of the X and Y axis for the right joystick

        :param: integer between -32768 and 32767 (0 = neutral position)
        """
        self._report.sThumbRX = x_value
        self._report.sThumbRY = y_value

    def left_joystick_float(self, x_value_float: float, y_value_float: float):
        """
        Sets the values of the X and Y axis for the left joystick

        :param: float between -1.0 and 1.0 (0 = neutral position)
        """
        self.left_joystick(round(x_value_float * 32767),
                           round(y_value_float * 32767))

    def right_joystick_float(self, x_value_float: float, y_value_float: float):
        """
        Sets the values of the X and Y axis for the right joystick

        :param: float between -1.0 and 1.0 (0 = neutral position)
        """
        self.right_joystick(round(x_value_float * 32767),
                            round(y_value_float * 32767))

    def _register_notification(self):
        check_err(_sdk.vigem_target_x360_register_notification(
            self._bus_pointer, self._device_pointer, self._callback_func, None))

    def unregister_notification(self):
        """
        Unregisters a previously registered callback function.
        """
        _sdk.vigem_target_x360_unregister_notification(self._device_pointer)
