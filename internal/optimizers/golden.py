import numpy as np
from typing import Callable

from internal.optimizers.base import BaseOptimizer, OptimisationResult
from internal.utils.decorators import validate_interval, count_calls

PHI = (np.sqrt(5) - 1) / 2


class GoldenSectionOptimizer(BaseOptimizer):
    def __init__(self, max_iterations: int = 10000):
        super().__init__(name="Golden Section")
        self.max_iterations = max_iterations

    @validate_interval
    def optimize(
        self, func: Callable[[float], float], a: float, b: float, epsilon: float, **kwargs
    ) -> OptimisationResult:
        if not hasattr(func, "calls"):
            func = count_calls(func)

        interval_history = [(a, b)]

        x1 = a + (1 - PHI) * (b - a)
        x2 = a + PHI * (b - a)
        f1 = func(x1)
        f2 = func(x2)

        n_iterations = 0

        while (b - a) > epsilon and n_iterations < self.max_iterations:
            n_iterations += 1

            if f1 < f2:
                b = x2
                x2 = x1
                f2 = f1
                x1 = a + (1 - PHI) * (b - a)
                f1 = func(x1)
            else:
                a = x1
                x1 = x2
                f1 = f2
                x2 = a + PHI * (b - a)
                f2 = func(x2)

            interval_history.append((a, b))

        if f1 < f2:
            x_opt = x1
            f_opt = f1
        else:
            x_opt = x2
            f_opt = f2

        return OptimisationResult(
            x_opt=x_opt,
            f_opt=f_opt,
            n_iterations=n_iterations,
            n_evaluations=func.calls,
            interval_history=interval_history,
        )
