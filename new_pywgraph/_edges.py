class Edge:

    def __init__(self, nodes: set[str]) -> None:
        if len(nodes) != 2:
            raise ValueError("Nodes must be a set of two nodes")

        self._nodes = nodes

    @property
    def nodes(self) -> set[str]:
        return self._nodes

    def __repr__(self) -> str:
        nodes_lst = list(self.nodes)
        node_0 = nodes_lst[0]
        node_1 = nodes_lst[1]
        return f"{node_0} -- {node_1}"

    def __hash__(self) -> int:
        return hash(frozenset(self.nodes))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Edge):
            return False
        return self.nodes == value.nodes


class DirectedEdge(Edge):
    def __init__(self, start: str, end: str) -> None:
        super().__init__(nodes={start, end})
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
        return DirectedEdge(self.end, self.start)

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, DirectedEdge):
            return False
        return self.start == value.start and self.end == value.end

    def __repr__(self) -> str:
        return f"{self.start} -> {self.end}"

    def __iter__(self):
        yield self.start
        yield self.end


class WeightedEdge(Edge):

    repr_precision: int = 2

    def __init__(self, nodes: set[str], weight: float) -> None:
        super().__init__(nodes)
        self._weight = weight

    @property
    def weight(self) -> float:
        return self._weight

    def __hash__(self) -> int:
        return hash((frozenset(self.nodes), self.weight))

    def __repr__(self) -> str:
        nodes_list = list(self.nodes)
        node_0 = nodes_list[0]
        node_1 = nodes_list[1]
        return f"{node_0} -({self.weight:.{self.repr_precision}})- {node_1}"
    
    def __iter__(self): 
        yield self.nodes
        yield self.weight


class WeightedDirectedEdge(DirectedEdge):

    repr_precision: int = 2

    def __init__(self, start: str, end: str, weight: float) -> None:
        super().__init__(start, end)
        self._weight = weight

    @property
    def weight(self) -> float:
        return self._weight
    
    @property
    def inverse(self) -> "WeightedDirectedEdge":
        return WeightedDirectedEdge(self.end, self.start, 1 / self.weight)

    def __hash__(self) -> int:
        return hash((self.start, self.end, self.weight))

    def __repr__(self) -> str:
        return f"{self.start} --({self.weight:.{self.repr_precision}})-> {self.end}"
    
    def __iter__(self):
        yield self.start
        yield self.end
        yield self.weight


if __name__ == "__main__":
    edge = Edge({"A", "B"})
    print(edge)

    directed_edge = DirectedEdge("A", "B")
    print(directed_edge)
    print(directed_edge.inverse)

    weighted_edge = WeightedEdge({"A", "B"}, 0.5)
    print(weighted_edge)
    
    weighted_directed_edge = WeightedDirectedEdge("A", "B", 0.5)
    print(weighted_directed_edge)
    print(weighted_directed_edge.inverse)
