from typing import Callable, Awaitable, ParamSpec, TypeVar, Concatenate, Any
from commons.error_handler import ModuleExceptionHandler
from commons.utils import get_module_name
from logging import getLogger
import inspect

_P = ParamSpec('_P')
_T = TypeVar('_T')

logger = getLogger(get_module_name(__file__))

_PreHandler = Callable[Concatenate[str, _P], Awaitable[None] | None]
_PostHandler = Callable[Concatenate[str, _T, _P], _T]

_default_exception_handler = ModuleExceptionHandler(get_module_name(__file__))


@_default_exception_handler.add_exception_handler(Exception)
def base_exception_handler(
    module: str,
    event: str,
    exception: Exception,
    args: tuple[Any, ...],
    kwargs: dict[str, Any]
):
    logger.error(
        f"{exception=} occured for {module=} {event=} with {args=} {kwargs=}"
    )


def task_decorator(
    exception_handler: ModuleExceptionHandler = _default_exception_handler,
    pre_handler: _PreHandler | None = None,
    post_handler: _PostHandler | None = None
):
    def core_task_decorator(func: Callable[_P, _T]):
        async def wrapper(*args: _P.args, **kwargs: _P.kwargs):
            async def core(*_args: _P.args, **_kwargs: _P.kwargs):
                if pre_handler:
                    pre = pre_handler(func.__name__, *_args, **_kwargs)
                    if inspect.isawaitable(pre):
                        pre = await pre
                return_val = func(*_args, **_kwargs)
                if inspect.isawaitable(return_val):
                    return_val = await return_val
                if post_handler:
                    return_val = post_handler(
                        func.__name__, return_val, *_args, **kwargs)
                    if inspect.isawaitable(return_val):
                        return_val = await return_val
                return return_val
            return await exception_handler.evaluate_with_exception_handler(
                func.__name__,
                core,
                *args,
                **kwargs
            )
        wrapper.__name__ = func.__name__

        return wrapper
    return core_task_decorator
