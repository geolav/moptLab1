from internal.functions import f3, f1, AsymmetricValleyFunction, PlateauFunction
from internal.optimizers import (DichotomyOptimizer, FibonacciOptimizer,
                                 GoldenSectionOptimizer, ParabolaOptimizer,
                                 PassiveSearchOptimizer, BrentOptimizer)
from internal.runner import run


def main() -> None:
    epsilons = [10 ** (-i) for i in range(1, 9)]
    a, b = -2.0, 5.0

    plateau = PlateauFunction(x_min=1.0, delta=0.8)
    plateau.__name__ = "PlateauFunction(x_min=1.0, δ=0.8)"

    asymmetric = AsymmetricValleyFunction(x_min=4.0, a=10.0, b=0.0)
    asymmetric.__name__ = "AsymmetricValley(x_min=4.0, a=10.0, b=0.0)"

    functions = [f1, f3, plateau, asymmetric]
    methods = [
        ("Пассивный поиск", PassiveSearchOptimizer()),
        ("Дихотомия", DichotomyOptimizer()),
        ("Золотое сечение", GoldenSectionOptimizer()),
        ("Фибоначчи", FibonacciOptimizer()),
        ("Парабола", ParabolaOptimizer()),
        ("Брент (SciPy)", BrentOptimizer()),
    ]

    run(
        functions=functions,
        methods=methods,
        a=a,
        b=b,
        epsilons=epsilons,
        output_root="results",
        save_graphs=True,
        save_tables=True,
    )

    print("\n" + "#" * 80)
    print(" МНОГОМОДАЛЬНАЯ ФУНКЦИЯ: СРАВНЕНИЕ С РАЗВЕДКОЙ ".center(80))
    print("#" * 80)

    eps = 1e-5

    golden = GoldenSectionOptimizer()
    passive = PassiveSearchOptimizer()

    #БЕЗ РАЗВЕДКИ
    res_no_search = golden.optimize(f3, a, b, eps)

    #С РАЗВЕДКОЙ
    res_passive = passive.optimize(f3, a, b, eps, n_points=1000)
    x0 = res_passive.x_opt

    delta = 0.5
    a_new = max(a, x0 - delta)
    b_new = min(b, x0 + delta)

    res_with_search = golden.optimize(f3, a_new, b_new, eps)

    print("\nБез разведки:")
    print(f"x* = {res_no_search.x_opt}, f(x*) = {res_no_search.f_opt}")

    print("\nС разведкой:")
    print(f"x* = {res_with_search.x_opt}, f(x*) = {res_with_search.f_opt}")

    print("\nИнтервал после разведки:")
    print(f"[{a_new}, {b_new}]")


if __name__ == "__main__":
    main()
