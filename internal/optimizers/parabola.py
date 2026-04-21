from typing import Callable
from internal.optimizers.base import BaseOptimizer, OptimisationResult
from internal.utils.decorators import ensure_counted


class ParabolaOptimizer(BaseOptimizer):
    def __init__(self, max_iterations: int = 1000):
        super().__init__(name="Парабола")
        self.max_iterations = max_iterations

    def optimize(
        self,
        func: Callable[[float], float],
        a: float,
        b: float,
        epsilon: float,
        **kwargs,
    ) -> OptimisationResult:
        counted_func = ensure_counted(func)

        x1 = a
        x3 = b
        x2 = (a + b) / 2

        f1 = counted_func(x1)
        f2 = counted_func(x2)
        f3 = counted_func(x3)

        if not (f1 > f2 and f2 < f3):
            x2 = (x1 + x3) / 2
            f2 = counted_func(x2)

        interval_history = [(x1, x3)]
        n_iterations = 0

        while n_iterations < self.max_iterations:
            n_iterations += 1

            numerator = (x2 - x1) ** 2 * (f2 - f3) - (x2 - x3) ** 2 * (f2 - f1)

            denominator = (x2 - x1) * (f2 - f3) - (x2 - x3) * (f2 - f1)

            if abs(denominator) < 1e-12:
                break

            u = x2 - 0.5 * numerator / denominator

            if not (x1 <= u <= x3):
                break

            fu = counted_func(u)

            if u < x2:
                if fu < f2:
                    x3, f3 = x2, f2
                    x2, f2 = u, fu
                else:
                    x1, f1 = u, fu
            else:
                if fu < f2:
                    x1, f1 = x2, f2
                    x2, f2 = u, fu
                else:
                    x3, f3 = u, fu

            interval_history.append((x1, x3))

            if abs(x3 - x1) < epsilon:
                break

        return OptimisationResult(
            x_opt=x2,
            f_opt=f2,
            n_iterations=n_iterations,
            n_evaluations=counted_func.calls,
            interval_history=interval_history,
        )
