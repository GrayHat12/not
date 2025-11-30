import sys
import os
from typing import TypeVar, overload, cast

_K = TypeVar('_K')
_V = TypeVar('_V')


def current_func_name(n: int = 0):
    return sys._getframe(n + 1).f_code.co_name


def get_module_name(file: str):
    return os.path.dirname(os.path.relpath(file)).replace('/', '.')


class BidirectionalMap(dict[_K, _V]):
    """
    Expects the keys and values to be a 1:1 mapping
    """

    def __init__(self, *args, **kwargs):

        super(BidirectionalMap, self).__init__(*args, **kwargs)
        self.__inverse: dict[_V, _K] = {}
        for key, value in self.items():
            self.__inverse[value] = key

    def __setitem__(self, key: _K, value: _V) -> None:
        if key in self:
            del self.__inverse[self[key]]
        if value in self.__inverse:
            raise KeyError(
                f"please maintain 1:1 mapping. {value=} already exists for key={self.__inverse[value]}")
        self.__inverse[value] = key
        return super().__setitem__(key, value)

    def __delitem__(self, key: _K) -> None:
        if key in self:
            del self.__inverse[self[key]]
        return super().__delitem__(key)

    @overload
    def __getitem__(self, key: _V) -> _K: ...
    @overload
    def __getitem__(self, key: _K) -> _V: ...

    def __getitem__(self, key: _K | _V) -> _V | _K:
        try:
            return super().__getitem__(cast(_K, key))
        except KeyError:
            return self.__inverse[cast(_V, key)]


if __name__ == "__main__":
    a = BidirectionalMap[str, int]()
    a["a"] = 1
    print(a["a"])
    print(a[1])
    a["b"] = 2
    print(a[2])
    a["c"] = 1
    print(a)
