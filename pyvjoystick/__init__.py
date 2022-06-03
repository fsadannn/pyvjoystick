from . import vigem, vjoy
from .vigem import *
from .vjoy import VJoyDevice

__all__ = ['vjoy', 'VJoyDevice', 'vigem']

__all__.extend(vigem.__all__)
