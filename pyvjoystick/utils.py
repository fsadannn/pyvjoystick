from typing import Callable


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
