from __future__ import annotations

from . import _sdk
from .utils import check_err


# We instantiate a single global VBus for all controllers
class VBus:
    """
    Virtual USB bus (ViGEmBus)
    """
    __slots__ = ('_bus_pointer',)
    __shared_instance: VBus = None

    @staticmethod
    def getVBus() -> VBus:
        """Static Access Method"""
        if VBus.__shared_instance is None:
            VBus()

        return VBus.__shared_instance

    def __init__(self):
        """virtual private constructor"""
        if VBus.__shared_instance is not None:
            raise Exception("This class is a singleton class !")
        else:
            VBus.__shared_instance = self

        self._bus_pointer = None

    def _init_bus(self):
        self._bus_pointer = _sdk.vigem_alloc()
        check_err(_sdk.vigem_connect(self._bus_pointer))

    @property
    def bus_pointer(self):
        if self._bus_pointer is None:
            self._init_bus()

        return self._bus_pointer

    def get_bus_pointer(self):
        if self._bus_pointer is None:
            self._init_bus()

        return self._bus_pointer

    def __del__(self):
        if self._bus_pointer is None:
            return

        _sdk.vigem_disconnect(self._bus_pointer)
        _sdk.vigem_free(self._bus_pointer)
