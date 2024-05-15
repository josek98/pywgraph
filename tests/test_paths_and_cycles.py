import pytest 
from pywgraph import Path, Cycle


def list_path() -> list[str]:
    return ["A", "B", "C", "D"]

def list_cycle() -> list[str]:
    return ["A", "B", "C", "A"]

def list_cycle_with_duplicates() -> list[str]:
    return ["A", "B", "C", "A", "B","A"]

def list_path_with_duplicates() -> list[str]:
    return ["A", "B", "C", "D", "A", "B"]

def list_invalid_path() -> list[str]:
    return ["A", "B", "B"]


class TestPathsAndCycles:

    def test_empty_path(self):
        with pytest.raises(ValueError):
            Path([])

    def test_empty_cycle(self):
        with pytest.raises(ValueError):
            Cycle([])

    def test_not_cycle(self):
        with pytest.raises(ValueError):
            Cycle(list_path())