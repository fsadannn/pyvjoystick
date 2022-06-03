from enum import Enum, IntEnum

DLL_FILENAME = "vJoyInterface.dll"
VJOY_REGISTRY_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{8E31F76F-74C3-47F1-9550-E041EEDC5FBB}_is1"
ARCH_64 = 'DllX64Location'
ARCH_86 = 'DllX86Location'


# HID Descriptor definitions(ported from public.h)
class HID_USAGE(IntEnum):
    X = 0x30
    Y = 0x31
    Z = 0x32
    RX = 0x33
    RY = 0x34
    RZ = 0x35
    SL0 = 0x36
    SL1 = 0x37
    WHL = 0x38
    POV = 0x39
    # V3
    ACCELERATOR = 0xC4
    BRAKE = 0xC5
    STEERING = 0xC6
    AILERON = 0xB0
    RUDDER = 0xBA
    THROTTLE = 0xBB


# for validity checking
HID_USAGE_LOW = HID_USAGE.X
HID_USAGE_HIGH = HID_USAGE.POV


# ported from VjdStat in vjoyinterface.h
class VJD_STATUS(IntEnum):
    OWN = 0  # The  vJoy Device is owned by this application.
    # The  vJoy Device is NOT owned by any application (including this one).
    FREE = 1
    # The  vJoy Device is owned by another application. It cannot be acquired by this application.
    BUSY = 2
    # The  vJoy Device is missing. It either does not exist or the driver is down.
    MISS = 3
    UNKN = 4  # Unknown


class JOYSTICK_API_VERSION(IntEnum):
    V1 = 1
    V2 = 2
    V3 = 3
