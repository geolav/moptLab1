from __future__ import annotations

from pathlib import Path
from typing import Callable, Sequence

from internal.utils.decorators import count_calls
from internal.utils.helpers import get_short_func_name
from internal.utils.visualization import plot_functions, print_table, _save_table_csv, plot_methods_comparison, \
    plot_all_interval_dynamics


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
        func_name = get_short_func_name(func.__name__)

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
            save_path=(plots_dir / f"{func_name}__comparison.png") if save_graphs else None,
        )
        plot_all_interval_dynamics(
            results_list,
            method_names,
            func.__name__,
            save_path=(plots_dir / f"{func_name}__interval_dynamics.png")
            if save_graphs
            else None,
        )

    if save_graphs:
        print(f"Графики сохранены в: {plots_dir}")
    if save_tables:
        print(f"Таблицы сохранены в: {tables_dir}")
