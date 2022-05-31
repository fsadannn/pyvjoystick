from typing import Dict, List

from . import _sdk
from .constants import HID_USAGE
from .exceptions import vJoyInvalid_rID_Exception


class Limits:
    __slots__ = ('minValue', 'maxValue', 'mean')

    def __init__(self, minValue: int, maxValue: int) -> None:
        self.minValue = minValue
        self.maxValue = maxValue
        self.mean = (maxValue + minValue) // 2

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}< minValue={self.minValue}, maxValue={self.maxValue} >'


class VJoyDevice:
    """Object-oriented API for a vJoy Device"""
    __slots__ = ('rID', '_data', 'available_axis',
                 'axis_limits', 'number_of_buttons')

    def __init__(self, rID: int = None, data=None):
        """Constructor"""

        self.rID = rID

        if rID > _sdk.GetvJoyMaxDevices() or rID <= 0:
            raise vJoyInvalid_rID_Exception

        if data:
            self._data = data
        else:
            # TODO maybe - have self.data as a wrapper object containing the Struct
            self._data = _sdk.CreateDataStructure(self.rID)

        _sdk.vJoyEnabled()
        _sdk.AcquireVJD(rID)
        _sdk.ResetVJD(rID)

        available_axis: List[HID_USAGE] = []
        axis_limits: Dict[HID_USAGE, Limits] = {}

        FIELDS_MAP = _sdk.FIELDS_MAP

        for hid in HID_USAGE:
            if _sdk.GetVJDAxisExist(rID, hid.value):
                try:
                    min_val = _sdk.GetVJDAxisMin(rID, hid.value)
                    max_val = _sdk.GetVJDAxisMax(rID, hid.value)
                except:
                    continue
                limit = Limits(minValue=min_val, maxValue=max_val)
                axis_limits[hid] = limit
                available_axis.append(hid)
                if hid in FIELDS_MAP:
                    setattr(self._data, FIELDS_MAP[hid], limit.mean)

        _sdk.UpdateVJD(rID, self._data)

        self.available_axis = available_axis
        self.axis_limits = axis_limits
        self.number_of_buttons = _sdk.GetVJDButtonNumber(rID)

    def set_button(self, buttonID, state):
        """Set a given button (numbered from 1) to On (1 or True) or Off (0 or False)"""
        return _sdk.SetBtn(state, self.rID, buttonID)

    def set_axis(self, AxisID, AxisValue):
        """Set a given Axis (one of pyvjoy.HID_USAGE_X etc) to a value (0x0000 - 0x8000)"""
        return _sdk.SetAxis(AxisValue, self.rID, AxisID)

    def set_disc_pov(self, PovID, PovValue):
        return _sdk.SetDiscPov(PovValue, self.rID, PovID)

    def set_cont_pov(self, PovID, PovValue):
        return _sdk.SetContPov(PovValue, self.rID, PovID)

    def reset(self):
        """Reset all axes and buttons to default values"""

        return _sdk.ResetVJD(self.rID)

    def reset_data(self):
        """Reset the data Struct to default (does not change vJoy device at all directly)"""
        self._data = _sdk.CreateDataStructure(self.rID)

    def reset_buttons(self):
        """Reset all buttons on the vJoy Device to default"""
        return _sdk.ResetButtons(self.rID)

    def reset_povs(self):
        """Reset all Povs on the vJoy Device to default"""
        return _sdk.ResetPovs(self.rID)

    def update(self):
        """Send the stored Joystick data to the device in one go (the 'efficient' method)"""
        return _sdk.UpdateVJD(self.rID, self._data)

    def read_data(self):
        """Read the stored Joystick data to the data structure"""
        return _sdk.GetPosition(self.rID, self._data)

    def __del__(self):
        # free up the controller before losing access
        _sdk.RelinquishVJD(self.rID)
