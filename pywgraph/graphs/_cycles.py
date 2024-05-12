from functools import cached_property

def _cycle_representations(cycle: list[str]) -> list[list[str]]:
    return [cycle[-i:] + cycle[:-i] for i in range(len(cycle))]

def _canonic_representation(cycle: list[str]) -> list[str]:
    first = min(cycle)
    canonic_representation = [
        representation
        for representation in _cycle_representations(cycle)
        if representation[0] == first
    ][0]
    return canonic_representation


class Cycle:

    def __init__(self, cycle: list[str]) -> None: 
        if len(cycle) < 2:
            raise ValueError("Cycle must have at least two elements")
        if cycle[0] == cycle[-1]:
            raise ValueError("Cycle can not contain equal consecutive elements")
        if any(cycle[i] == cycle[i+1] for i in range(len(cycle) - 1)):
            raise ValueError("Cycle can not contain equal consecutive elements")

        self._cycle = cycle

    @cached_property
    def cycle(self) -> list[str]:
        return _canonic_representation(self._cycle)
    
    @cached_property
    def equivalent_representations(self) -> list[list[str]]:
        return _cycle_representations(self._cycle)
    
    def __len__(self) -> int:
        return len(self._cycle)
    
    def __hash__(self) -> int:
        return hash(tuple(self.cycle))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cycle):
            if len(other) != len(self):
                return False
            return other.cycle in self.equivalent_representations
        return False
    
    def __repr__(self) -> str:
        return f"Cycle({self.cycle})"