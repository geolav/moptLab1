from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, List, Tuple

@dataclass
class OptimisationResult:
    x_opt: float
    f_opt: float
    n_iterations: int
    n_evaluations: int
    interval_history: List[Tuple[float, float]] = field(default_factory=list)

class BaseOptimizer(ABC):
    def __init__(self, name: str = "BaseOptimizer"):
        self.name = name

    @abstractmethod
    def optimize(
        self, func: Callable[[float], float], a: float, b: float, epsilon: float, **kwargs
    ) -> OptimisationResult:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
