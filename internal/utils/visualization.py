import csv

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Callable, Optional
from internal.utils.helpers import get_short_func_name
from pathlib import Path

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

def print_table(results: list[dict], method_name: str, func_name: str) -> None:
    print(f"\n{'=' * 80}")
    print(f"  {method_name} | {func_name}")
    print(f"{'=' * 80}")
    print(f"{'eps':>12} | {'x*':>12} | {'f(x*)':>14} | {'итер.':>6} | {'вычисл.':>8}")
    print(f"{'-' * 80}")

    for result in results:
        n_iterations = result["n_iterations"] if result["n_iterations"] != -1 else "N/A"
        print(
            f"{result['eps']:>12.1e} | {result['x_opt']:>12.8f} | "
            f"{result['f_opt']:>14.10e} | {str(n_iterations):>6} | "
            f"{result['n_evaluations']:>8}"
        )

    print(f"{'=' * 80}\n")


def plot_methods_comparison(
    results_list: list[list[dict]],
    method_names: list[str],
    func_name: str,
    save_path: Path | None = None,
) -> None:
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    for results, method_name in zip(results_list, method_names):
        eps = [res["eps"] for res in results]
        n_iter = [res["n_iterations"] for res in results]
        n_eval = [res["n_evaluations"] for res in results]

        ax1.plot(eps, n_iter, marker="o", label=method_name, linewidth=2)
        ax2.plot(eps, n_eval, marker="s", label=method_name, linewidth=2)

    ax1.set_xscale("log")
    ax1.set_xlabel("Epsilon (ε)", fontsize=12)
    ax1.set_ylabel("Количество итераций", fontsize=12)
    ax1.set_title(f"Итерации vs Точность на {func_name}", fontsize=13)
    ax1.invert_xaxis()
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.set_xscale("log")
    ax2.set_xlabel("Epsilon (ε)", fontsize=12)
    ax2.set_ylabel("Количество вычислений", fontsize=12)
    ax2.set_title(f"Вычисления vs Точность на {func_name}", fontsize=13)
    ax2.invert_xaxis()
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


def plot_all_interval_dynamics(
    results_list: list[list[dict]],
    method_names: list[str],
    func_name: str,
    save_path: Path | None = None,
) -> None:
    n_methods = len(results_list)
    n_cols = min(3, n_methods)
    n_rows = int(np.ceil(n_methods / n_cols))
    _, axes = plt.subplots(n_rows, n_cols, figsize=(6 * n_cols, 5 * n_rows), squeeze=False)
    flat_axes = axes.ravel()

    for idx, (results, method_name) in enumerate(zip(results_list, method_names)):
        ax = flat_axes[idx]
        has_data = False
        for j, result in enumerate(results):
            if j % 2 != 0:
                continue

            history = result["history"]
            if not history:
                continue

            a_vals = [h[0] for h in history]
            b_vals = [h[1] for h in history]
            iterations = range(len(history))

            ax.plot(
                iterations,
                a_vals,
                "o--",
                markersize=3,
                alpha=0.7,
                label=f'a, ε={result["eps"]:.0e}',
            )
            ax.plot(
                iterations,
                b_vals,
                "s-",
                markersize=3,
                alpha=0.7,
                label=f'b, ε={result["eps"]:.0e}',
            )
            has_data = True

        ax.set_xlabel("Итерация", fontsize=11)
        ax.set_ylabel("Границы интервала", fontsize=11)
        ax.set_title(f"{method_name} на {func_name}", fontsize=12)
        ax.grid(True, alpha=0.3)
        if has_data:
            ax.legend(fontsize=9)
        else:
            ax.text(0.5, 0.5, "Нет данных", ha="center", va="center", transform=ax.transAxes)

    for ax in flat_axes[n_methods:]:
        ax.axis("off")

    plt.tight_layout()
    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


def plot_functions(
    functions: list[Callable[[float], float]],
    a: float,
    b: float,
    save_path: Path | None = None,
) -> None:
    x = np.linspace(a, b, 1000)
    n_funcs = len(functions)
    _, axes = plt.subplots(1, n_funcs, figsize=(6 * n_funcs, 5))

    if n_funcs == 1:
        axes = [axes]

    for i, func in enumerate(functions):
        y = [func(x_i) for x_i in x]
        axes[i].plot(x, y, linewidth=2)
        axes[i].set_title(f"Функция: {func.__name__}", fontsize=13)
        axes[i].set_xlabel("x", fontsize=11)
        axes[i].set_ylabel("f(x)", fontsize=11)
        axes[i].grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()



def _save_table_csv(
    results: list[dict],
    method_name: str,
    func_name: str,
    output_dir: Path,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    file_name = f"{get_short_func_name(func_name)}__{method_name.replace(' ', '_')}.csv"
    file_path = output_dir / file_name

    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["epsilon", "x_opt", "f_opt", "n_iterations", "n_evaluations"])
        for result in results:
            writer.writerow(
                [
                    result["eps"],
                    result["x_opt"],
                    result["f_opt"],
                    result["n_iterations"],
                    result["n_evaluations"],
                ]
            )

    return file_path