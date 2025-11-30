import sys
import os


def current_func_name(n: int = 0):
    return sys._getframe(n + 1).f_code.co_name


def get_module_name(file: str):
    return os.path.dirname(os.path.relpath(file)).replace('/', '.')
