# Copyright (c) 2017 TitanSnow; All Rights Reserved


from typing import Iterable, Callable, Any

def quote():
    raise NotImplementedError()

class AcceptArgGenerator:
    """
    class AcceptArgGenerator
    special callable base class for LispMachine that accepts arg generator
    """
    def __call__(self, args: Iterable) -> Any:
        """`args` is the arg generator passed by LispMachine"""
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
            try:
                symbol = next(it)
            except StopIteration:
                return (x for x in range(0))
            func = _resolve_func(symbol)
            if func is quote:
                return next(it)
            def get_args() -> Iterable:
                while True:
                    item = next(it)
                    yield _eval(item) if _isevalable(item) else item
            return func(*get_args()) if not isinstance(func, AcceptArgGenerator) else func(get_args())
        return _eval(lst)

class and_(AcceptArgGenerator):
    def __call__(self, lst: Iterable) -> bool:
        it = iter(lst)
        try:
            while True:
                if not next(it):
                    return False
        except StopIteration:
            return True
and_ = and_()

class or_(AcceptArgGenerator):
    def __call__(self, lst: Iterable) -> bool:
        it = iter(lst)
        try:
            while True:
                if next(it):
                    return True
        except StopIteration:
            return False
or_ = or_()

lst = lambda *args: args
