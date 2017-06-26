# Copyright (c) 2017 TitanSnow; All Rights Reserved


from typing import Iterable, Callable, Any

def quote():
    raise NotImplementedError()

class LispMachine:
    """class LispMachine"""
    functable = {}
    def eval(self, lst: Iterable) -> Any:
        """eval `lst`"""
        def _isevalable(lst: Any) -> bool:
            return isinstance(lst, Iterable) and not isinstance(lst, str) and not isinstance(lst, bytes)
        def _resolve_func(symbol: Any) -> Callable:
            if isinstance(symbol, Callable):
                return symbol
            if isinstance(symbol, str):
                return self.functable[symbol]
            if _isevalable(symbol):
                return _resolve_func(_eval(symbol))
        def _eval(lst: Iterable) -> Any:
            it = iter(lst)
            func = _resolve_func(next(it))
            if func is quote:
                return next(it)
            def get_args() -> Iterable:
                while True:
                    item = next(it)
                    yield _eval(item) if _isevalable(item) else item
            return func(*get_args())
        return _eval(lst)
