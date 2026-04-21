import numpy as np
from typing import Callable
from internal.optimizers.base import BaseOptimizer, OptimisationResult
from internal.utils.decorators import ensure_counted


class PassiveSearchOptimizer(BaseOptimizer):
    def __init__(self):
        super().__init__(name="Пассивный поиск")

    def optimize(
        self,
        func: Callable[[float], float],
        a: float,
        b: float,
        epsilon: float,
        **kwargs,
    ) -> OptimisationResult:
        n_points = kwargs.get("n_points", None)
        if n_points is None:
            n_points = min(max(int(np.ceil((b - a) / epsilon)), 2), 100000)

        x_values = np.linspace(a, b, n_points)

        counted_func = ensure_counted(func)
        f_values = np.array([counted_func(x) for x in x_values])
        n_evaluations = counted_func.calls

        min_idx = np.argmin(f_values)
        x_opt = x_values[min_idx]
        f_opt = f_values[min_idx]

        interval_history = [(a, b)]

        return OptimisationResult(
            x_opt=x_opt,
            f_opt=f_opt,
            n_iterations=1,
            n_evaluations=n_evaluations,
            interval_history=interval_history,
        )
