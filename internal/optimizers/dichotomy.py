from typing import Callable

from internal.optimizers.base import OptimisationResult


class DichotomyOptimizer:

    name = "Дихотомия"

    def optimize(
            self, func: Callable[[float], float], a: float, b: float, epsilon: float
    ) -> OptimisationResult:
        delta = epsilon / 2
        n_iterations = 0
        interval_history: list[tuple[float, float]] = []

        while (b - a) / 2 > epsilon:
            n_iterations += 1
            x1 = (a + b - delta) / 2
            x2 = (a + b + delta) / 2
            f1 = func(x1)
            f2 = func(x2)
            interval_history.append((a, b))

            if f1 <= f2:
                b = x2
            else:
                a = x1

        x_opt = (a + b) / 2
        return OptimisationResult(
            x_opt=x_opt,
            f_opt=func(x_opt),
            n_iterations=n_iterations,
            n_evaluations=getattr(func, "calls", 0),
            interval_history=interval_history,
        )