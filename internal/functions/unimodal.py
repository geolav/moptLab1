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

class AsymmetricValleyFunction:
    def __init__(self, x_min: float = 4.0, a: float = 10.0, b: float = 0.0):
        self.x_min = x_min
        self.degree = int(a)
        self.b = b
        self.__name__ = f"AsymmetricValleyFunction(x_min={x_min}, degree={self.degree})"

    def __call__(self, x: float) -> float:
        return abs(x - self.x_min)**self.degree + self.b

    def global_minimum(self) -> tuple[float, float]:
        return self.x_min, self.b