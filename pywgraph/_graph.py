import numpy as np
from ._edge import WeightedDirectedEdge  # type: ignore
from ._exceptions import NodeNotFound  # type: ignore


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

    def __repr__(self) -> str:
        return f"WeightedDirectedGraph(nodes={self._nodes}, edges={self._edges})"


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
