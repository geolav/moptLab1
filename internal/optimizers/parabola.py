# import numpy as np
# from typing import Callable, Optional, Tuple
#
# from internal.optimizers.base import BaseOptimizer, OptimisationResult
# from internal.utils.decorators import count_calls
#
#
# class ParabolaOptimizer(BaseOptimizer):
#     def __init__(self, max_iterations: int = 1000, min_improvement: float = 1e-10):
#         super().__init__(name="Parabola Method")
#         self.max_iterations = max_iterations
#         self.min_improvement = min_improvement
#
#     def _fit_parabola(
#         self, x1: float, f1: float, x2: float, f2: float, x3: float, f3: float
#     ) -> Optional[float]:
#         denom = (x2 - x1) * (f2 - f3) - (x2 - x3) * (f2 - f1)
#
#         if abs(denom) < 1e-12:
#             return None
#
#         numer = (x2 - x1) ** 2 * (f2 - f3) - (x2 - x3) ** 2 * (f2 - f1)
#         x_new = x2 - 0.5 * numer / denom
#
#         return x_new
#
#     def optimize(
#         self, func: Callable[[float], float], a: float, b: float, epsilon: float, **kwargs
#     ) -> OptimisationResult:
#         if not hasattr(func, "calls"):
#             func = count_calls(func)
#
#         interval_history = [(a, b)]
#
#         x1 = a
#         x2 = (a + b) / 2
#         x3 = b
#
#         f1 = func(x1)
#         f2 = func(x2)
#         f3 = func(x3)
#
#         points = [(x1, f1), (x2, f2), (x3, f3)]
#         points.sort(key=lambda p: p[1])
#         x_best, f_best = points[0]
#
#         n_iterations = 0
#
#         while n_iterations < self.max_iterations:
#             n_iterations += 1
#
#             x_new = self._fit_parabola(x1, f1, x2, f2, x3, f3)
#
#             # if x_new is None or not (a <= x_new <= b):
#             #     if f1 < f3:
#             #         x_new = x1 + 0.382 * (x2 - x1)
#             #     else:
#             #         x_new = x2 + 0.382 * (x3 - x2)
#
#             if x_new is None or not (a <= x_new <= b):
#                 # Теперь при неудаче параболы мы не делаем умный шаг,
#                 # а просто берем середину текущего интервала.
#                 # Это гораздо менее эффективно на плоских функциях.
#                 x_new = (a + b) / 2.0
#
#             x_new = np.clip(x_new, a, b)
#             f_new = func(x_new)
#
#             if x_new < x2:
#                 if f_new < f2:
#                     x3, f3 = x2, f2
#                     x2, f2 = x_new, f_new
#                 else:
#                     x1, f1 = x_new, f_new
#             else:
#                 if f_new < f2:
#                     x1, f1 = x2, f2
#                     x2, f2 = x_new, f_new
#                 else:
#                     x3, f3 = x_new, f_new
#
#             improvement = abs(f_best - f2) / (abs(f_best) + 1e-12)
#
#             if f2 < f_best:
#                 x_best, f_best = x2, f2
#
#             if improvement < self.min_improvement:
#                 break
#
#             a_curr = min(x1, x2, x3)
#             b_curr = max(x1, x2, x3)
#             interval_history.append((a_curr, b_curr))
#
#             if abs(b_curr - a_curr) < epsilon:
#                 break
#
#             if max(abs(x2 - x1), abs(x3 - x2)) < epsilon:
#                 break
#
#         return OptimisationResult(
#             x_opt=x_best,
#             f_opt=f_best,
#             n_iterations=n_iterations,
#             n_evaluations=func.calls,
#             interval_history=interval_history,
#         )




# =================================================================
#  версия по конспекту.
from typing import Callable

from internal.optimizers.base import BaseOptimizer, OptimisationResult
from internal.utils.decorators import count_calls


class ParabolaOptimizer(BaseOptimizer):
    def __init__(self, max_iterations: int = 1000):
        super().__init__(name="Parabola Method")
        self.max_iterations = max_iterations

    def optimize(
        self,
        func: Callable[[float], float],
        a: float,
        b: float,
        epsilon: float,
        **kwargs
    ) -> OptimisationResult:

        if not hasattr(func, "calls"):
            func = count_calls(func)

        # начальные точки
        x1 = a
        x3 = b
        x2 = (a + b) / 2

        f1 = func(x1)
        f2 = func(x2)
        f3 = func(x3)

        # гарантируем условие унимодальности
        if not (f1 > f2 and f2 < f3):
            # если не выполнено — чуть сдвигаем x2
            x2 = (x1 + x3) / 2
            f2 = func(x2)

        interval_history = [(x1, x3)]
        n_iterations = 0

        while n_iterations < self.max_iterations:
            n_iterations += 1

            # формула вершины параболы
            numerator = (
                (x2 - x1) ** 2 * (f2 - f3)
                - (x2 - x3) ** 2 * (f2 - f1)
            )

            denominator = (
                (x2 - x1) * (f2 - f3)
                - (x2 - x3) * (f2 - f1)
            )

            if abs(denominator) < 1e-12:
                break

            u = x2 - 0.5 * numerator / denominator

            # если вышли за границы — ломаемся
            if not (x1 <= u <= x3):
                break

            fu = func(u)

            # обновление тройки точек
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

            # критерий остановки
            if abs(x3 - x1) < epsilon:
                break

        return OptimisationResult(
            x_opt=x2,
            f_opt=f2,
            n_iterations=n_iterations,
            n_evaluations=func.calls,
            interval_history=interval_history,
        )