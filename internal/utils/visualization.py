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


def plot_convergence(
    results: List[Dict],
    method_name: str,
    func_name: str,
    save_path: Optional[str] = None,
) -> plt.Figure:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    epsilons = [r["eps"] for r in results]
    iterations = [r["n_iterations"] for r in results]
    evaluations = [r["n_evaluations"] for r in results]

    ax1.semilogx(epsilons, iterations, "o-", linewidth=2, markersize=6)
    ax1.set_xlabel("Точность ε (логарифмическая шкала)", fontsize=12)
    ax1.set_ylabel("Количество итераций", fontsize=12)
    ax1.set_title(f"{method_name} - Итерации vs Точность", fontsize=13)
    ax1.grid(True, alpha=0.3)
    ax1.invert_xaxis()

    ax2.semilogx(epsilons, evaluations, "s-", linewidth=2, markersize=6, color="orange")
    ax2.set_xlabel("Точность ε (логарифмическая шкала)", fontsize=12)
    ax2.set_ylabel("Количество вычислений", fontsize=12)
    ax2.set_title(f"{method_name} - Вычисления vs Точность", fontsize=13)
    ax2.grid(True, alpha=0.3)
    ax2.invert_xaxis()

    fig.suptitle(f"{method_name} на {func_name}", fontsize=15, fontweight="bold")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig


def plot_interval_dynamics(
    interval_history: List[Tuple[float, float]],
    method_name: str,
    func_name: str,
    true_minimum: Optional[float] = None,
    save_path: Optional[str] = None,
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(12, 6))

    iterations = range(len(interval_history))
    left_bounds = [interval[0] for interval in interval_history]
    right_bounds = [interval[1] for interval in interval_history]

    ax.plot(iterations, left_bounds, "o-", label="Левая граница (a)", linewidth=2, markersize=5)
    ax.plot(iterations, right_bounds, "s-", label="Правая граница (b)", linewidth=2, markersize=5)

    ax.fill_between(iterations, left_bounds, right_bounds, alpha=0.2)

    if true_minimum is not None:
        ax.axhline(
            y=true_minimum,
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"Истинный минимум: {true_minimum:.4f}",
        )

    ax.set_xlabel("Итерация", fontsize=12)
    ax.set_ylabel("Границы интервала", fontsize=12)
    ax.set_title(
        f"{method_name} - Динамика интервала на {func_name}", fontsize=14, fontweight="bold"
    )
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig


def plot_comparison(
    results_dict: Dict[str, List[Dict]],
    func_name: str,
    metric: str = "n_evaluations",
    save_path: Optional[str] = None,
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(12, 7))

    for method_name, results in results_dict.items():
        epsilons = [r["eps"] for r in results]
        values = [r[metric] for r in results]
        ax.loglog(epsilons, values, "o-", label=method_name, linewidth=2, markersize=6)

    ax.set_xlabel("Точность ε (логарифмическая шкала)", fontsize=12)
    ylabel = "Количество итераций" if metric == "n_iterations" else "Количество вычислений"
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(f"Сравнение методов на {func_name}", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, which="both")
    ax.invert_xaxis()

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig


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


def visualize_all_results(
    results_dict: Dict[str, Dict[str, List[Dict]]], output_dir: str = "results"
):
    import os

    os.makedirs(output_dir, exist_ok=True)

    for method_name, func_results in results_dict.items():
        for func_name, results in func_results.items():
            plot_convergence(
                results,
                method_name,
                func_name,
                save_path=f"{output_dir}/{method_name}_{func_name}_convergence.png",
            )
            plt.close()

            if results and "history" in results[0]:
                history = results[0]["history"]
                plot_interval_dynamics(
                    history,
                    method_name,
                    func_name,
                    save_path=f"{output_dir}/{method_name}_{func_name}_intervals.png",
                )
                plt.close()
