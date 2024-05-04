from math import prod
from ._edge import WeightedDirectedEdge  # type: ignore
from ._exceptions import NodeNotFound  # type: ignore
from ._utils import _find_path


class WeightedDirectedGraph:
    def __init__(self, nodes: set[str], edges: set[WeightedDirectedEdge]) -> None:
        self._nodes = nodes
        self._edges = edges

    @property
    def nodes(self) -> set[str]:
        return self._nodes

    @property
    def edges(self) -> set[WeightedDirectedEdge]:
        return self._edges

    def check_definition(self) -> bool:
        """Checks if the graph is defined correctly."""
        bad_starters = {
            edge.start for edge in self._edges if edge.start not in self._nodes
        }
        bad_enders = {edge.end for edge in self._edges if edge.end not in self._nodes}
        if len(bad_starters | bad_enders) != 0:
            print(
                f"Following nodes where not found in the graph nodes: {bad_starters | bad_enders}"
            )
            return False
        return True

    def children(self, node: str) -> set[str]:
        """Returns the children of a node."""
        if node not in self._nodes:
            raise NodeNotFound(node)
        return {edge.end for edge in self._edges if edge.start == node}

    def parents(self, node: str) -> set[str]:
        """Returns the parents of a node."""
        if node not in self._nodes:
            raise NodeNotFound(node)
        return {edge.start for edge in self._edges if edge.end == node}

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
        return prod(path_edges_weights)
    
    def weight_between(self, start: str, end: str) -> float:
        """Returns the weight of the shortest path between two nodes."""
        path = self.find_path(start, end)
        return self.path_weight(path)

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

    def __repr__(self) -> str:
        return f"WeightedDirectedGraph(nodes={self._nodes}, edges={self._edges})"

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
