from math import prod
from ._groups import Group
from ._edge import WeightedDirectedEdge  # type: ignore
from ._exceptions import NodeNotFound  # type: ignore
from ._utils import _find_path

_default_group = Group(
    "Real numbers with multiplication", 1.0, lambda x, y: x * y, lambda x, y: x / y
)


def _check_nodes_in_edges(
    nodes: set[str],
    edges: set[WeightedDirectedEdge],
) -> bool:
    edge_nodes = set().union(*[{edge.start, edge.end} for edge in edges])
    return edge_nodes <= nodes


class WeightedDirectedGraph:
    def __init__(
        self,
        nodes: set[str],
        edges: set[WeightedDirectedEdge],
        group: Group = _default_group,
    ) -> None:
        self._nodes = nodes
        self._edges = edges
        self._group = group

    @property
    def nodes(self) -> set[str]:
        return self._nodes

    @property
    def edges(self) -> set[WeightedDirectedEdge]:
        return self._edges

    @property
    def group(self) -> Group:
        return self._group

    #Working with group
    def check_definition(self) -> bool:
        """Checks if the graph is defined correctly."""
        return _check_nodes_in_edges(self.nodes, self.edges)

    #Working with group
    def children(self, node: str) -> set[str]:
        """Returns the children of a node."""
        if node not in self._nodes:
            raise NodeNotFound(node)
        return {edge.end for edge in self._edges if edge.start == node}

    #Working with group
    def parents(self, node: str) -> set[str]:
        """Returns the parents of a node."""
        if node not in self._nodes:
            raise NodeNotFound(node)
        return {edge.start for edge in self._edges if edge.end == node}

    #Working with group
    def add_reverse_edges(self, inplace: bool = False):
        """Adds the missing inverse direction edges"""

        all_inverse_edges = {edge.inverse for edge in self._edges}
        inverse_edges = {
            edge
            for edge in all_inverse_edges
            if edge.start not in self.parents(edge.end)
        }
        if inplace:
            self._edges.update(inverse_edges)
            return

        return WeightedDirectedGraph(self._nodes, self._edges | inverse_edges)

    #Working with group
    def find_path(self, start: str, end: str) -> list[str]:
        """Finds a path between two nodes."""
        uknown_nodes = {start, end} - self.nodes
        if uknown_nodes:
            raise NodeNotFound(uknown_nodes)
        return _find_path(self, start, end)

    def path_weight(self, path: list[str]) -> float:
        """Returns the weight of following the given path in the graph"""
        if not path:
            return 0.0

        uknown_nodes = set(path) - self.nodes
        if uknown_nodes:
            raise NodeNotFound(uknown_nodes)
        path_pairs = list(zip(path, path[1::]))
        path_edges_weights = [
            edge.weight for edge in self.edges if (edge.start, edge.end) in path_pairs
        ]
        if len(path_pairs) != len(path_edges_weights):
            raise ValueError(f"The path {path} is not a valid path in the graph")
        return prod(path_edges_weights)

    def weight_between(self, start: str, end: str) -> float:
        """Returns the weight of the shortest path between two nodes."""
        path = self.find_path(start, end)
        return self.path_weight(path)

    # This will need to add the underlying group of the weights
    @classmethod
    def from_dict(cls, dict: dict[str, dict[str, float]]) -> "WeightedDirectedGraph":
        """Creates a graph from a dictionary."""
        nodes = set(dict.keys())
        edges = {
            WeightedDirectedEdge(start, end, weight)
            for start, end_dict in dict.items()
            for end, weight in end_dict.items()
        }
        return cls(nodes, edges)

    #Working with group
    def __repr__(self) -> str:
        nodes_str = f"Nodes: {self.nodes}\n"
        edges_str = f"Edges:\n"
        for edge in self.edges:
            edges_str += f"{edge}\n"
        return nodes_str + edges_str

    #Working with group
    def __eq__(self, other: object) -> bool:
        if isinstance(other, WeightedDirectedGraph):
            return self._nodes == other._nodes and self._edges == other._edges
        return False


if __name__ == "__main__":
    nodes = {"A", "B", "C", "D", "E"}
    edges = {
        WeightedDirectedEdge("A", "B", 1),
        WeightedDirectedEdge("A", "C", 2),
        WeightedDirectedEdge("B", "D", 3),
        WeightedDirectedEdge("E", "A", 4),
    }

    graph = WeightedDirectedGraph(nodes, edges)
    print(graph)
    print(graph.children("E"))
    print(graph.parents("B"))
