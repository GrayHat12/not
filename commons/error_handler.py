from typing import Type, Callable, Awaitable, TypeVar, Any, ParamSpec
from functools import partial
import inspect

T = TypeVar('T', bound=Exception)
R = TypeVar('R')
P = ParamSpec('P')

_ExceptionHandler = Callable[
    [str, str, T, tuple[Any, ...], dict[str, Any]],
    Awaitable[None] | None
]

_HandlerGroup = tuple[tuple[Type[T], ...], _ExceptionHandler[T]]
_ModuleHandler = list[_HandlerGroup[T]]

_Registry = dict[str, _ModuleHandler[T]]

_REGISTERED_HANDLERS: _Registry = {}


def register_exception_handler(module_name: str, handler: _ExceptionHandler[T], *exception_type: Type[T]):
    global _REGISTERED_HANDLERS
    if module_name not in _REGISTERED_HANDLERS:
        _REGISTERED_HANDLERS[module_name] = []

    _REGISTERED_HANDLERS[module_name].append((exception_type, handler))


def add_exception_handler(module_name: str, *exception_type: Type[T]):
    def decorator(func: _ExceptionHandler[T]):
        register_exception_handler(module_name, func, *exception_type)
        return func
    return decorator


async def evaluate_with_exception_handler(
    module_name: str,
    event_name: str,
    eval_func: Callable[P, Awaitable[R]],
    *args: P.args,
    **kwargs: P.kwargs
):
    try:
        return await eval_func(*args, **kwargs)
    except Exception as e:
        if module_name not in _REGISTERED_HANDLERS:
            raise e
        for (exception_group, handler) in _REGISTERED_HANDLERS[module_name]:
            if isinstance(e, exception_group):
                handled = handler(module_name, event_name, e, args, kwargs)
                if inspect.isawaitable(handled):
                    handled = await handled
                return handled
        raise e


class ModuleExceptionHandler():
    def __init__(self, module_name: str) -> None:
        self.register_exception_handler = partial(
            register_exception_handler, module_name)
        self.add_exception_handler = partial(
            add_exception_handler, module_name)
        self.evaluate_with_exception_handler = partial(
            evaluate_with_exception_handler, module_name)
