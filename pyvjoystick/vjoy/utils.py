import sys
import warnings
import winreg
from pathlib import Path
from platform import architecture
from typing import Callable

from .constants import ARCH_64, ARCH_86, JOYSTICK_API_VERSION, VJOY_REGISTRY_PATH


def is64bits() -> bool:
    return '64' in architecture()[0]


def get_dll_path() -> str:
    access_registry: winreg.HKEYType = winreg.ConnectRegistry(
        None, winreg.HKEY_LOCAL_MACHINE)
    try:
        access_key: winreg.HKEYType = winreg.OpenKey(
            access_registry, VJOY_REGISTRY_PATH)
    except OSError:
        sys.exit("vJoy does not appear to be installed.Please ensure you have installed vJoy from http://vjoystick.sourceforge.net.")

    install_location: str = winreg.QueryValueEx(
        access_key, 'InstallLocation')[0]

    if is64bits():
        arch_location = ARCH_64
    else:
        arch_location = ARCH_86

    try:
        dll_location: str = winreg.QueryValueEx(access_key, arch_location)[0]
    except FileNotFoundError:
        warnings.warn(
            'A vJoy install was found, but it appears to be an old version. Please update vJoy to the latest version from nhttp://vjoystick.sourceforge.net')

        if is64bits():
            dll_location = str(Path(install_location) / 'x64')
        else:
            dll_location = str(Path(install_location) / 'x86')

    return dll_location


def get_api_version() -> JOYSTICK_API_VERSION:
    access_registry: winreg.HKEYType = winreg.ConnectRegistry(
        None, winreg.HKEY_LOCAL_MACHINE)
    try:
        access_key: winreg.HKEYType = winreg.OpenKey(
            access_registry, VJOY_REGISTRY_PATH)
    except OSError:
        sys.exit("vJoy does not appear to be installed.Please ensure you have installed vJoy from http://vjoystick.sourceforge.net.")

    version: str = winreg.QueryValueEx(
        access_key, 'DisplayVersion')[0]

    major, minor, *_ = version.split('.')

    if int(major) < 2:
        return JOYSTICK_API_VERSION.V1

    if int(minor) < 2:
        return JOYSTICK_API_VERSION.V2

    return JOYSTICK_API_VERSION.V3


class lazy_eval:
    __slots__ = ('_func', '_context', '_variable_name', '_args', '_kwargs')

    def __init__(self, context: dict, variable_name: str, func: Callable, *args, **kwargs):
        self._func = func
        self._context = context
        self._variable_name = variable_name
        self._args = args
        self._kwargs = kwargs

    def __getattr__(self, attr):
        print(f'get arrt {attr}')
        result = self._func(*self._args, **self._kwargs)
        updated_context = {self._variable_name: result}

        self._context.update(updated_context)

        return getattr(result, attr)
