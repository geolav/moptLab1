import math


def f3(x: float) -> float:
    return (x - 1.5) ** 2 + math.sin(5 * x)


f3.__name__ = "(x-1.5)^2 + sin(5x)"

