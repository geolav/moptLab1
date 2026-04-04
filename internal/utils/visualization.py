import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Callable, Tuple, Optional

sns.set_style("whitegrid")
sns.set_palette("husl")


def plot_function(
    func: Callable[[float], float],
    a: float,
    b: float,
    n_points: int = 1000,
    ax: Optional[plt.Axes] = None,
    label: Optional[str] = None,
) -> plt.Axes:
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    x = np.linspace(a, b, n_points)
    y = np.array([func(xi) for xi in x])

    func_name = label or getattr(func, "__name__", "f(x)")
    ax.plot(x, y, linewidth=2, label=func_name)
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("f(x)", fontsize=12)
    ax.set_title(f"Функция: {func_name}", fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    return ax


def create_results_table(results: List[Dict], method_name: str, func_name: str) -> str:
    lines = ["=" * 80, f"  {method_name} на {func_name}", "=" * 80,
             f"{'ε':>12} | {'x*':>12} | {'f(x*)':>14} | {'Итер':>6} | {'Вычисл':>6}", "-" * 80]

    for r in results:
        n_iter = r["n_iterations"] if r["n_iterations"] != -1 else "N/A"
        lines.append(
            f"{r['eps']:>12.1e} | {r['x_opt']:>12.8f} | {r['f_opt']:>14.10e} | "
            f"{str(n_iter):>6} | {r['n_evaluations']:>6}"
        )

    lines.append("=" * 80)
    return "\n".join(lines)
