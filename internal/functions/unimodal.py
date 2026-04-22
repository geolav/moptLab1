def plateau_function(x: float) -> float:
    x_min = 1.0
    delta = 0.8
    x_shifted = x - x_min
    if abs(x_shifted) <= delta:
        return delta**2
    return x_shifted**2


plateau_function.__name__ = "plateau_function"


def asymmetric_function(x: float) -> float:
    if x < 3:
        return (x - 3) ** 2
    return (x - 3) ** 4


asymmetric_function.__name__ = "asymmetric_function"
