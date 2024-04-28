import numpy as np


class DirectedEdge:
    def __init__(self, start: str, end: str) -> None:
        self._start = start
        self._end = end

    @property
    def start(self) -> str:
        return self._start

    @property
    def end(self) -> str:
        return self._end
    
    @property
    def inverse(self) -> "DirectedEdge":
        return DirectedEdge(self._end, self._start)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DirectedEdge):
            return self._start == other.start and self._end == other.end
        return False

    def __repr__(self) -> str:
        return f"{self._start} -> {self._end}"


class WeightedDirectedEdge(DirectedEdge):
    def __init__(self, start: str, end: str, weight: float | np.ndarray[float]) -> None:
        super().__init__(start, end)
        self._weight = weight

    @property
    def weight(self) -> float | np.ndarray[float]:
        return self._weight

    @property
    def inverse(self) -> "WeightedDirectedEdge":
        return WeightedDirectedEdge(self._end, self._start, 1 / self._weight)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, WeightedDirectedEdge):
            return super().__eq__(other) and np.array_equal(self._weight, other.weight)
        return False

    def __repr__(self) -> str:
        return super().__repr__() + f": {self._weight}"


if __name__ == "__main__":
    edge = WeightedDirectedEdge("A", "B", np.array([1, 2, 3]))
    print(edge)
    print(edge.inverse)
