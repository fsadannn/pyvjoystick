import sys
from ctypes import CDLL, Structure, c_byte, c_int, c_long, cdll, pointer, wintypes
from pathlib import Path
from typing import Dict

from ..utils import lazy_eval
from .constants import DLL_FILENAME, HID_USAGE, JOYSTICK_API_VERSION, VJD_STATUS
from .exceptions import (
    vJoyButtonException,
    vJoyDriverMismatchException,
    vJoyException,
    vJoyFailedToAcquireException,
    vJoyFailedToRelinquishException,
    vJoyInvalidAxisException,
    vJoyInvalidAxisValueException,
    vJoyInvalidPovIDException,
    vJoyInvalidPovValueException,
    vJoyNotEnabledException,
)
from .utils import get_api_version, get_dll_path

_dll_path = str(Path(get_dll_path()) / DLL_FILENAME)


def _load_sdk(_dll_path: str):
    try:
        _vj: CDLL = cdll.LoadLibrary(_dll_path)
    except OSError:
        sys.exit("Unable to load vJoy SDK DLL.  Ensure that %s is present" %
                 DLL_FILENAME)


# lazy load sdk, is loaded the first time is used
_vj = lazy_eval(locals(), '_vj', _load_sdk, _dll_path)


def GetNumberExistingVJD() -> int:
    """Return the number of vJoy devices currently enabled"""
    data = c_int(0)

    _vj.GetNumberExistingVJD(pointer(data))

    return data.value


def GetvJoyMaxDevices() -> int:
    """Return the maximum possible number of vJoy devices"""
    data = c_int(0)

    _vj.GetvJoyMaxDevices(pointer(data))

    return data.value


def vJoyEnabled():
    """Returns True if vJoy is installed and enabled"""

    result = _vj.vJoyEnabled()

    if result == 0:
        raise vJoyNotEnabledException
    else:
        return True


def DriverMatch():
    """Check if the version of vJoyInterface.dll and the vJoy Driver match"""
    result = _vj.DriverMatch()

    if result == 0:
        raise vJoyDriverMismatchException
    else:
        return True


def GetVJDStatus(rID) -> VJD_STATUS:
    """Get the status of a given vJoy Device"""
    status: int = _vj.GetVJDStatus(rID)

    return list(VJD_STATUS)[status]


def AcquireVJD(rID):
    """Attempt to acquire a vJoy Device"""

    result = _vj.AcquireVJD(rID)
    if result == 0:
        # Check status
        status = GetVJDStatus(rID)
        if status != VJD_STATUS.FREE:
            raise vJoyFailedToAcquireException(
                f"Cannot acquire vJoy Device because it is not in FREE({status})")

        else:
            raise vJoyFailedToAcquireException(f"Status {status}")

    else:
        return True


def RelinquishVJD(rID):
    """Relinquish control of a vJoy Device"""

    result = _vj.RelinquishVJD(rID)
    if result == 0:
        raise vJoyFailedToRelinquishException
    else:
        return True


def GetVJDButtonNumber(rID: int) -> int:
    """Get the number of buttons defined in the specified VDJ"""
    return _vj.GetVJDButtonNumber(rID)


def GetVJDDiscPovNumber(rID: int) -> int:
    """Get the number of discrete-type POV hats defined in the specified VDJ"""
    return _vj.GetVJDDiscPovNumber(rID)


def GetVJDContPovNumber(rID: int) -> int:
    """Get the number of continue-type POV hats defined in the specified VDJ"""
    return _vj.GetVJDContPovNumber(rID)


def GetVJDAxisExist(rID: int, AxisId: int) -> bool:
    """Test if given axis defined in the specified VDJ"""
    result = _vj.GetVJDAxisExist(rID, AxisId)

    if result == 0:
        return False

    return True


def GetVJDAxisMax(rID: int, AxisId: int) -> int:
    """Get logical Maximum value for a given axis defined in the specified VDJ"""
    data = c_long(0)

    result = _vj.GetVJDAxisMax(rID, AxisId, pointer(data))

    if result == 0:
        # TODO: check in what cases the function return false
        raise vJoyException

    return data.value


def GetVJDAxisMin(rID: int, AxisId: int) -> int:
    """Get logical Minimum value for a given axis defined in the specified VDJ"""
    data = c_long(0)

    result = _vj.GetVJDAxisMin(rID, AxisId, pointer(data))

    if result == 0:
        # TODO: check in what cases the function return false
        raise vJoyException

    return data.value


def SetBtn(state, rID, buttonID):
    """Sets the state of a vJoy Button to on or off.  SetBtn(state,rID,buttonID)"""
    result = _vj.SetBtn(state, rID, buttonID)
    if result == 0:
        raise vJoyButtonException
    else:
        return True


def SetAxis(AxisValue, rID, AxisID, validate: bool = False):
    """Sets the value of a vJoy Axis  SetAxis(value,rID,AxisID)"""

    if validate:
        if not GetVJDAxisExist(rID, AxisID):
            raise vJoyInvalidAxisException

        if GetVJDAxisMin(rID, AxisID) > AxisValue or GetVJDAxisMax(rID, AxisID) < AxisValue:
            raise vJoyInvalidAxisValueException

    result = _vj.SetAxis(AxisValue, rID, AxisID)
    if result == 0:
        # TODO raise specific exception
        raise vJoyException
    else:
        return True


def SetDiscPov(PovValue, rID, PovID):
    """Write Value to a given discrete POV defined in the specified VDJ"""
    if PovValue < -1 or PovValue > 3:
        raise vJoyInvalidPovValueException

    if PovID < 1 or PovID > 4:
        raise vJoyInvalidPovIDException

    return _vj.SetDiscPov(PovValue, rID, PovID)


def SetContPov(PovValue, rID, PovID):
    """Write Value to a given continuous POV defined in the specified VDJ"""
    if PovValue < -1 or PovValue > 35999:
        raise vJoyInvalidPovValueException

    if PovID < 1 or PovID > 4:
        raise vJoyInvalidPovIDException

    return _vj.SetContPov(PovValue, rID, PovID)


def ResetVJD(rID):
    """Reset all axes and buttons to default for specified vJoy Device"""
    return _vj.ResetVJD(rID)


def ResetAll():
    """Reset all controls to predefined values in all VDJ"""
    return _vj.ResetAll()


def ResetButtons(rID):
    """Reset all buttons to default (To 0) for specified vJoy Device"""
    return _vj.ResetButtons(rID)


def ResetPovs(rID):
    """Reset all POV hats to default (To -1) for specified vJoy Device"""
    return _vj.ResetPovs(rID)


def UpdateVJD(rID, data):
    """Pass data for all buttons and axes to vJoy Device efficiently"""
    return _vj.UpdateVJD(rID, pointer(data))


def GetPosition(rID, data):
    """V3 only. Read the position data of the specified vJoy Device"""
    return _vj.GetPosition(rID, pointer(data))


def CreateDataStructure(rID):
    version = get_api_version()

    if version == JOYSTICK_API_VERSION.V3:
        data = _JOYSTICK_POSITION_V3()
    elif version == JOYSTICK_API_VERSION.V2:
        data = _JOYSTICK_POSITION_V2()
    else:
        data = _JOYSTICK_POSITION_V1()

    data.set_defaults(rID)
    return data


FIELDS_MAP: Dict[HID_USAGE, str] = {
    HID_USAGE.X: 'wAxisX',
    HID_USAGE.Y: 'wAxisY',
    HID_USAGE.Z: 'wAxisZ',
    HID_USAGE.RX: 'wAxisXRot',
    HID_USAGE.RY: 'wAxisYRot',
    HID_USAGE.RZ: 'wAxisZRot',
}

_v1_fields = [
    # Index of device. 1 - based.
    ('bDevice', c_byte),
    ('wThrottle', c_long),
    ('wRudder', c_long),
    ('wAileron', c_long),
    ('wAxisX', c_long),
    ('wAxisY', c_long),
    ('wAxisZ', c_long),
    ('wAxisXRot', c_long),
    ('wAxisYRot', c_long),
    ('wAxisZRot', c_long),
    ('wSlider', c_long),
    ('wDial', c_long),
    ('wWheel', c_long),
    ('wAxisVX', c_long),
    ('wAxisVY', c_long),
    ('wAxisVZ', c_long),
    ('wAxisVBRX', c_long),
    ('wAxisVRBY', c_long),
    ('wAxisVRBZ', c_long),
    # 32 buttons: 0x00000001 means button1 is pressed, 0x80000000 -> button32 is pressed
    ('lButtons', c_long),

    # Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
    ('bHats', wintypes.DWORD),
    # Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
    ('bHatsEx1', wintypes.DWORD),
    # Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
    ('bHatsEx2', wintypes.DWORD),
    # Lower 4 bits: HAT switch or 16-bit of continuous HAT switch LONG lButtonsEx1
    ('bHatsEx3', wintypes.DWORD)
]

_v2_fields = _v1_fields.copy()
_v2_fields.extend([
    # JOYSTICK_POSITION_V2 Extension
    ('lButtonsEx1', c_long),  # Buttons 33-64
    ('lButtonsEx2', c_long),  # Buttons 65-96
    ('lButtonsEx3', c_long),  # Buttons 97-128
])

_v3_fields = [
    # JOYSTICK_POSITION
    # Index of device. 1-based.
    ('bDevice', c_byte),

    ('wThrottle', c_long),
    ('wRudder', c_long),
    ('wAileron', c_long),

    ('wAxisX', c_long),
    ('wAxisY', c_long),
    ('wAxisZ', c_long),
    ('wAxisXRot', c_long),
    ('wAxisYRot', c_long),
    ('wAxisZRot', c_long),
    ('wSlider', c_long),
    ('wDial', c_long),

    ('wWheel', c_long),
    # V3 new fields
    ('wAccelerator', c_long),
    ('wBrake', c_long),
    ('wClutch', c_long),
    ('wSteering', c_long),

    ('wAxisVX', c_long),
    ('wAxisVY', c_long),

    # 32 buttons: 0x00000001 means button1 is pressed, 0x80000000 -> button32 is pressed
    ('lButtons', c_long),

    # Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
    ('bHats', wintypes.DWORD),
    # Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
    ('bHatsEx1', wintypes.DWORD),
    # Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
    ('bHatsEx2', wintypes.DWORD),
    # Lower 4 bits: HAT switch or 16-bit of continuous HAT switch LONG lButtonsEx1
    ('bHatsEx3', wintypes.DWORD),

    # JOYSTICK_POSITION_V2 Extension
    ('lButtonsEx1', c_long),  # Buttons 33-64
    ('lButtonsEx2', c_long),  # Buttons 65-96
    ('lButtonsEx3', c_long),  # Buttons 97-128

    # JOYSTICK Extension V3: replacing old slots and moving them at the tail
    ('wAxisVZ', c_long),
    ('wAxisVBRX', c_long),
    ('wAxisVRBY', c_long),
    ('wAxisVRBZ', c_long),

]


class _JOYSTICK_POSITION_V1(Structure):
    _fields_ = _v1_fields

    def set_defaults(self, rID):

        self.bDevice = c_byte(rID)
        self.bHats = -1


class _JOYSTICK_POSITION_V2(Structure):
    _fields_ = _v2_fields

    def set_defaults(self, rID):

        self.bDevice = c_byte(rID)
        self.bHats = -1


class _JOYSTICK_POSITION_V3(Structure):
    _fields_ = _v3_fields

    def set_defaults(self, rID):

        self.bDevice = c_byte(rID)
        self.bHats = -1
