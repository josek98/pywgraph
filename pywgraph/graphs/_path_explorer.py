class PathExplorer:

    def __init__(self, path: list[str] = [], visited: set[str] = set()):
        self._path = path
        self._visited = visited

    @property
    def path(self) -> list[str]:
        return self._path

    @property
    def visited(self) -> set[str]:
        return self._visited

    def __hash__(self) -> int:
        return hash((tuple(self.path), tuple(self.visited)))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PathExplorer):
            return (self.path, self.visited) == (other.path, other.visited)
        return False

    def __repr__(self) -> str:
        return f"PathExplorer({self._path}, {self._visited})"

    def __len__(self) -> int:
        return len(self._path)
