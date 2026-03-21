import numpy as np
import matplotlib.pyplot as plt


# f1 = TODO
# f1.__name__ = "<function in string view>" TODO
# f2 = TODO
# f2.__name__ = "<function in string view>" TODO
# f3 = TODO
# f3.__name__ = "<function in string view>" TODO


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
            'nth_iter':  res.n_iterations,
            'nth_eval':  res.n_evaluations,
            'history': res.interval_history,
        })
    return results

def print_table(results, method_name, func_name):
    print(f"\n{'=' * 60}")
    print(f"\t{method_name}\t|\t{func_name}")
    print(f"\n{'=' * 60}")
    print(f"{'eps':>10} | {'x*':>10} | {'f(x*)':>12} | {'итер.':>6} | {'вычисл.':>8}")
    print(f"\n{'-' * 60}")
    for res in results:
        nth_iter = res['nth_iter'] if res['nth_iter']!= -1 else 'n/f'
        print(f"{res['eps']:>10.1e} | {res['x_opt']:>10.6f} | "
              f"{res['f_opt']:>12.8f} | {str(nth_iter):>6} | {res['nth_eval']:>8}")


# if __name__ == "__main__":
    # TODO:
    # passive = <class()>
    # dichotomy =
    # gold =
    # fibonacci =
    # parabola =
    # brent =

    # epsilons = []