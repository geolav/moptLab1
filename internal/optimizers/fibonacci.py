from typing import Callable
from internal.optimizers.base import BaseOptimizer, OptimisationResult


class FibonacciOptimizer(BaseOptimizer):
    def __init__(self) -> None:
        super().__init__(name="Фибоначчи")

    @staticmethod
    def build_fib_sequence(limit: float) -> list[int]:
        fib_numbers = [0, 1, 1]
        while fib_numbers[-1] < limit:
            fib_numbers.append(fib_numbers[-1] + fib_numbers[-2])
        fib_numbers.append(fib_numbers[-1] + fib_numbers[-2])
        return fib_numbers

    def optimize(
        self,
        func: Callable[[float], float],
        a: float,
        b: float,
        epsilon: float,
        **kwargs,
    ) -> OptimisationResult:
        fib_numbers = self.build_fib_sequence((b - a) / epsilon)
        n = len(fib_numbers) - 2

        n_iterations = 0
        interval_history: list[tuple[float, float]] = []
        k = 1
        lam = a + (fib_numbers[n - k] / fib_numbers[n - k + 2]) * (b - a)
        mu = a + (fib_numbers[n - k + 1] / fib_numbers[n - k + 2]) * (b - a)
        f_lam = func(lam)
        f_mu = func(mu)

        while k < n - 1:
            n_iterations += 1
            interval_history.append((a, b))

            if f_lam > f_mu:
                a = lam
                lam = mu
                f_lam = f_mu
                k += 1
                mu = a + (fib_numbers[n - k + 1] / fib_numbers[n - k + 2]) * (b - a)
                f_mu = func(mu)
            else:
                b = mu
                mu = lam
                f_mu = f_lam
                k += 1
                lam = a + (fib_numbers[n - k] / fib_numbers[n - k + 2]) * (b - a)
                f_lam = func(lam)

        mu = min(lam + epsilon, b)
        f_mu = func(mu)
        if f_lam > f_mu:
            a = lam
        else:
            b = mu

        x_opt = (a + b) / 2
        return OptimisationResult(
            x_opt=x_opt,
            f_opt=func(x_opt),
            n_iterations=n_iterations,
            n_evaluations=getattr(func, "calls", 0),
            interval_history=interval_history,
        )
