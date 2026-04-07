class PlateauFunction:

    def __init__(self, x_min: float = 0.0, delta: float = 0.1):
        self.x_min = x_min
        self.delta = delta
        self.__name__ = f"PlateauFunction(x_min={x_min}, δ={delta})"

    def __call__(self, x: float) -> float:
        x_shifted = x - self.x_min
        if abs(x_shifted) <= self.delta:
            return self.delta**2
        else:
            return x_shifted**2

    def global_minimum(self) -> tuple[float, float]:
        return self.x_min, self.delta**2


# class AsymmetricValleyFunction:
#
#     def __init__(self, x_min: float = 0.0, a: float = 2.0, b: float = 0.0):
#         self.x_min = x_min
#         self.a = a
#         self.b = b
#         self.__name__ = f"AsymmetricValley(x_min={x_min}, a={a}, b={b})"
#
#         self._actual_min = x_min - 3 * a / 4
#
#     def __call__(self, x: float) -> float:
#         x_shifted = x - self.x_min
#         return x_shifted**4 + self.a * x_shifted**3 + self.b
#
#     def global_minimum(self) -> tuple[float, float]:
#         x_opt = self._actual_min
#         return x_opt, self(x_opt)

class AsymmetricValleyFunction:
    def __init__(self, x_min: float = 4.0, a: float = 10.0, b: float = 0.0):
        # Теперь параметр 'a' мы используем как степень функции (например, 10)
        self.x_min = x_min
        self.degree = int(a)
        self.b = b
        # Имя для графиков
        self.__name__ = f"TrapFunction(x_min={x_min}, degree={self.degree})"

    def __call__(self, x: float) -> float:
        # Чем выше степень, тем сложнее методу парабол найти вершину
        return abs(x - self.x_min)**self.degree + self.b

    def global_minimum(self) -> tuple[float, float]:
        return self.x_min, self.b