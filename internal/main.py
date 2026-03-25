import math

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field

# f1 = TODO
def f1(x):
    return (x - 2)**2 + 1
f1.__name__ = "(x-2)^2 + 1"
# f1.__name__ = "<function in string view>" TODO
# f2 = TODO
# f2.__name__ = "<function in string view>" TODO
# f3 = TODO
def f3(x):
    return (x - 1.5)**2 + math.sin(5 * x)
f3.__name__ = "(x-1.5)^2 + sin(5x)"
# f3.__name__ = "<function in string view>" TODO

# mb template for returning by optimisation classes
@dataclass
class OptimisationResult:
    x_opt: float
    f_opt: float
    n_iterations: int
    n_evaluations: int
    interval_history: list = field(default_factory=list)

class Dichotomy:
    def optimize(self, f, a, b, eps):
        delta = eps / 2
        iters = 0
        history = []
        while (b - a) / 2 > eps:
            iters += 1
            x1 = (a + b - delta) / 2
            x2 = (a + b + delta) / 2
            f_1 = f(x1)
            f_2 = f(x2)
            history.append((a, b))
            if f_1 <= f_2:
                b = x2
            else:
                a = x1

        x_opt = (a + b) / 2
        return OptimisationResult(
            x_opt = x_opt,
            f_opt = f(x_opt),
            n_iterations = iters,
            n_evaluations = f.calls,
            interval_history = history
        )


class Fibonacci:
    def fib(self, n):
        a, b = 1, 1
        for _ in range(n - 1):
            a = b
            b = a + b
        return a
    def optimize(self, f, a, b, eps):
        n = 1
        while self.fib(n) < (b - a) / eps:
            n += 1
        iters = 0
        history = []
        k = 1
        lam = a + (self.fib(n - k) / self.fib(n - k + 2)) * (b - a)
        mu = a + (self.fib(n - k + 1) / self.fib(n - k + 2)) * (b - a)
        f_lam = f(lam)
        f_mu = f(mu)

        while k < n - 1:
            iters += 1
            history.append((a, b))
            if f_lam > f_mu:
                a = lam
                lam = mu
                f_lam = f_mu
                k += 1
                mu = a + (self.fib(n - k + 1) / self.fib(n - k + 2)) * (b - a)
                f_mu = f(mu)
            else:
                b = mu
                mu = lam
                f_mu = f_lam
                k += 1
                lam = a + (self.fib(n - k) / self.fib(n - k + 2)) * (b - a)
                f_lam = f(lam)

        mu = lam + eps
        f_mu = f(mu)
        if f_lam > f_mu:
            a = lam
        else:
            b = mu
        x_opt = (a + b) / 2
        return OptimisationResult(
            x_opt = x_opt,
            f_opt = f(x_opt),
            n_iterations = iters,
            n_evaluations = f.calls,
            interval_history = history
        )


def count_calls(f):
    def caller(x):
        caller.calls += 1
        return f(x)
    caller.calls = 0
    caller.__name__ = f.__name__
    return caller

def run_optimizer(optimizer, f, a, b, epsilons):
    results = []
    for eps in epsilons:
        f.calls = 0
        res = optimizer.optimize(f, a, b, eps)
        results.append({
            'eps':     eps,
            'x_opt':   res.x_opt,
            'f_opt':   res.f_opt,
            'n_iterations':  res.n_iterations,
            'n_evaluations':  res.n_evaluations,
            'history': res.interval_history,
        })
    return results

def print_table(results, method_name, func_name):
    print(f"\n{'=' * 60}")
    print(f"\t{method_name}\t|\t{func_name}")
    print(f"{'=' * 60}")
    print(f"{'eps':>10} | {'x*':>10} | {'f(x*)':>12} | {'итер.':>6} | {'вычисл.':>8}")
    print(f"{'-' * 60}")
    for res in results:
        n_iter = res['n_iterations'] if res['n_iterations']!= -1 else 'n/f'
        print(f"{res['eps']:>10.1e} | {res['x_opt']:>10.6f} | "
              f"{res['f_opt']:>12.8f} | {str(n_iter):>6} | {res['n_evaluations']:>8}")

def plot_iters_evals(results_list, method_name, func_name):
    plt.figure(figsize=(12, 6))
    for i, results in enumerate(results_list):
        eps = [res['eps'] for res in results]
        n_iter = [res['n_iterations'] for res in results]
        n_eval = [res['n_evaluations'] for res in results]

        plt.subplot(1, len(results_list), i + 1)
        plt.plot(eps, n_iter, marker='o', label="Iterations")
        plt.plot(eps, n_eval, marker='x', label="Evaluations")
        plt.xscale('log')
        plt.xlabel('Epsilon')
        plt.ylabel('Count')
        plt.title(f"{method_names[i]} method on {func_name}")
        plt.gca().invert_xaxis()
        plt.legend()
        plt.grid()
    plt.tight_layout()
    plt.show()

def plot_interval_dynamics(results_list, method_names, func_name):
    plt.figure(figsize=(12, 6))
    for i, results in enumerate(results_list):
        plt.subplot(1, len(results_list), i + 1)
        for j, res in enumerate(results):
            if j % 2 == 0:
                history = res['history']
                if not history:
                    continue
                a_vals = [h[0] for h in history]
                b_vals = [h[1] for h in history]
                plt.plot(range(len(history)), a_vals, label=f'a, eps={res["eps"]}')
                plt.plot(range(len(history)), b_vals, label=f'b, eps={res["eps"]}')
        plt.xlabel("Iterations")
        plt.ylabel("Interval boundaries")
        plt.title(f"{method_names[i]} method on {func_name}")
        plt.legend()
        plt.grid()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # passive = <class()>
    dichotomy = Dichotomy()
    # gold =
    fibonacci = Fibonacci()
    # parabola =
    # brent =

    epsilons = [10**(-1), 10**(-2), 10**(-3), 10**(-4), 10**(-5), 10**(-6), 10**(-7), 10**(-8)]

    a, b = -2, 5

    functions = [f1, f3]
    methods = [
        ("Dichotomy", dichotomy),
        ("Fibonacci", fibonacci),
    ]

    for func in functions:
        wrapped_f = count_calls(func)
        results_list = []
        method_names = []
        for name, method in methods:
            results = run_optimizer(method, wrapped_f, a, b, epsilons)
            results_list.append(results)
            method_names.append(name)
            print_table(results, name, func.__name__)

        plot_iters_evals(results_list, method_names, func.__name__)
        plot_interval_dynamics(results_list, method_names, func.__name__)

    x = np.linspace(a, b, 1000)

    plt.figure(figsize=(12, 6))
    for i, func in enumerate(functions):
        y = [func(x_i) for x_i in x]
        plt.subplot(1, len(functions), i + 1)
        plt.plot(x, y)
        plt.title(f"Function: {func.__name__}")
        plt.grid()

    plt.show()