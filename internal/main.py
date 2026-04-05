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

    asymmetric = AsymmetricValleyFunction(x_min=4.0, a=3.0, b=0.0)
    asymmetric.__name__ = "AsymmetricValley(x_min=4.0, a=3.0, b=0.0)"

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


if __name__ == "__main__":
    main()
