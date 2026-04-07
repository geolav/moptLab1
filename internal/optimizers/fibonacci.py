from typing import Callable

from internal.optimizers.base import OptimisationResult


class FibonacciOptimizer:

    name = "Фибоначчи"

    def fib(self, n: int) -> int:
        a, b = 1, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return a

    def optimize(
        self, func: Callable[[float], float], a: float, b: float, epsilon: float
    ) -> OptimisationResult:
        n = 1
        while self.fib(n) < (b - a) / epsilon:
            n += 1

        n_iterations = 0
        interval_history: list[tuple[float, float]] = []
        k = 1
        lam = a + (self.fib(n - k) / self.fib(n - k + 2)) * (b - a)
        mu = a + (self.fib(n - k + 1) / self.fib(n - k + 2)) * (b - a)
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
                mu = a + (self.fib(n - k + 1) / self.fib(n - k + 2)) * (b - a)
                f_mu = func(mu)
            else:
                b = mu
                mu = lam
                f_mu = f_lam
                k += 1
                lam = a + (self.fib(n - k) / self.fib(n - k + 2)) * (b - a)
                f_lam = func(lam)

        mu = lam + epsilon
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

