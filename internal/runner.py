from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Callable, Sequence

import matplotlib.pyplot as plt
import numpy as np

from internal.utils.decorators import count_calls


def _slugify(name: str) -> str:
    slug = re.sub(r"\s+", "_", name.strip().lower())
    slug = re.sub(r"[^\w\-\.]+", "_", slug)
    return slug.strip("_") or "item"


def _save_table_csv(
    results: list[dict],
    method_name: str,
    func_name: str,
    output_dir: Path,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    file_name = f"{_slugify(func_name)}__{_slugify(method_name)}.csv"
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


def run_optimizer(
    optimizer: object,
    func: Callable[[float], float],
    a: float,
    b: float,
    epsilons: Sequence[float],
) -> list[dict]:
    results: list[dict] = []
    for epsilon in epsilons:
        func.calls = 0
        result = optimizer.optimize(func, a, b, epsilon)
        results.append(
            {
                "eps": epsilon,
                "x_opt": result.x_opt,
                "f_opt": result.f_opt,
                "n_iterations": result.n_iterations,
                "n_evaluations": result.n_evaluations,
                "history": result.interval_history,
            }
        )
    return results


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


def run(
    functions: list[Callable[[float], float]],
    methods: list[tuple[str, object]],
    a: float,
    b: float,
    epsilons: Sequence[float],
    output_root: str = "results",
    save_graphs: bool = True,
    save_tables: bool = True,
) -> None:
    root = Path(output_root)
    plots_dir = root / "plots"
    tables_dir = root / "tables"

    print("\nПостроение графиков функций...")
    plot_functions(
        functions,
        a,
        b,
        save_path=(plots_dir / "all_functions.png") if save_graphs else None,
    )

    for func in functions:
        print(f"\n{'#' * 80}")
        print(f" Тестирование на функции: {func.__name__} ".center(80))
        print(f"{'#' * 80}\n")

        wrapped_func = count_calls(func)
        results_list: list[list[dict]] = []
        method_names: list[str] = []
        func_slug = _slugify(func.__name__)

        for method_name, method in methods:
            print(f"Запуск {method_name}...")
            results = run_optimizer(method, wrapped_func, a, b, epsilons)
            results_list.append(results)
            method_names.append(method_name)
            print_table(results, method_name, func.__name__)

            if save_tables:
                table_path = _save_table_csv(results, method_name, func.__name__, tables_dir)
                print(f"Сохранена таблица: {table_path}")

        print(f"Построение сравнительных графиков для {func.__name__}...")
        plot_methods_comparison(
            results_list,
            method_names,
            func.__name__,
            save_path=(plots_dir / f"{func_slug}__comparison.png") if save_graphs else None,
        )
        plot_all_interval_dynamics(
            results_list,
            method_names,
            func.__name__,
            save_path=(plots_dir / f"{func_slug}__interval_dynamics.png")
            if save_graphs
            else None,
        )

    if save_graphs:
        print(f"Графики сохранены в: {plots_dir}")
    if save_tables:
        print(f"Таблицы сохранены в: {tables_dir}")
