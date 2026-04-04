from typing import Callable

from scipy.optimize import minimize_scalar

from internal.optimizers.base import BaseOptimizer, OptimisationResult


class BrentOptimizer(BaseOptimizer):
    def __init__(self, max_iterations: int = 10000):
        super().__init__(name="Brent")
        self.max_iterations = max_iterations

    def optimize(
        self, func: Callable[[float], float], a: float, b: float, epsilon: float, **kwargs
    ) -> OptimisationResult:
        result = minimize_scalar(
            func,
            method="brent",
            bracket=(a, b),
            tol=epsilon,
            options={"maxiter": self.max_iterations},
        )

        return OptimisationResult(
            x_opt=float(result.x),
            f_opt=float(result.fun),
            n_iterations=int(getattr(result, "nit", -1)),
            n_evaluations=int(getattr(result, "nfev", 0)),
            interval_history=[],
        )

