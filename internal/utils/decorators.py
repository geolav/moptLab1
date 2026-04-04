import functools
from typing import Callable, Any


class FunctionCallCounter:

    def __init__(self, func: Callable[[float], float]):
        self.func = func
        self.calls = 0
        self.__name__ = getattr(func, "__name__", repr(func))
        self.__doc__ = func.__doc__

    def __call__(self, x: float) -> float:
        self.calls += 1
        return self.func(x)

    def reset(self) -> None:
        self.calls = 0


def count_calls(func: Callable[[float], float]) -> FunctionCallCounter:
    return FunctionCallCounter(func)


def validate_interval(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(
        self, objective_func: Callable, a: float, b: float, epsilon: float, **kwargs
    ) -> Any:
        if a >= b:
            raise ValueError(f"Недопустимый интервал: a ({a}) должно быть меньше b ({b})")
        return func(self, objective_func, a, b, epsilon, **kwargs)

    return wrapper
