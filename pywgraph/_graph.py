from functools import reduce  # type: ignore
from ._groups import Group
from ._edge import WeightedDirectedEdge  # type: ignore
from ._exceptions import NodeNotFound, NodeAlreadyExists, EdgeAlreadyExists  # type: ignore
from ._utils import _find_path

_default_group = Group(
    "Real numbers under multiplication", 1.0, lambda x, y: x * y, lambda x: 1 / x
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

    def check_definition(self) -> bool:
        """Checks if the graph is defined correctly."""
        return _check_nodes_in_edges(self.nodes, self.edges)

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

    def add_node(self, node: str, inplace: bool = False):
        """Adds a node to the graph"""
        if node in self._nodes:
            raise NodeAlreadyExists(node)
        if inplace:
            self._nodes.add(node)
            return

        return_graph = WeightedDirectedGraph(
            nodes=self._nodes | {node}, edges=self._edges, group=self.group
        )
        return return_graph

    def delete_node(self, node: str, inplace: bool = False):
        """Deletes a node from the graph. Also removes all edges connected to this node."""
        if node not in self._nodes:
            raise NodeNotFound(node)

        node_edges = {
            edge for edge in self._edges if edge.start == node or edge.end == node
        }
        good_edges = self.edges - node_edges

        if inplace:
            self._nodes.remove(node)
            self._edges = good_edges
            return

        return_graph = WeightedDirectedGraph(
            nodes=self._nodes - {node}, edges=good_edges, group=self.group
        )
        return return_graph

    def add_edge(
        self,
        start: str,
        end: str,
        weight: "Group.element" = None,
        path: list[str] | None = None,
        allow_inverse: bool = True,
        inplace: bool = False,
    ):
        """Adds an edge connectingh two existing nodes.

        Parameter
        --------
        start: str
            The start node of the edge. Must be an existing node from the graph.
        end: str
            The end node of the edge. Must be an existing node from the graph.
        weight: Optional[Group.element]
            The weight of the edge. If no weight and not path is provided, the weight will be try
            to be calculated finding a path connecting the edges.
        path: Optional[list[str]]
            If this is provided and no weight is given the weight will be calculated using this path.
            If this path is not possible and exception will be raised. It is possible to use
            a path that exists but does not connect start and end node, this might be removed
            in future versions.
        allow_inverse: bool
            If True, allows the creation of the inverse edge to find a path between edges.
        """

        bad_nodes = {start, end} - self._nodes
        if bad_nodes:
            raise NodeNotFound(bad_nodes)
        if (start, end) in {(edge.start, edge.end) for edge in self._edges}:
            raise EdgeAlreadyExists(start, end)

        if weight is None:  # Find weight in another way
            if allow_inverse:
                search_graph = self.add_reverse_edges(inplace=False)
            else:
                search_graph = self

            if path is not None:  # Apply weight of the given path
                weight = search_graph.path_weight(path)
            else:  # Find path to get a weight
                path = search_graph.find_path(start, end)
                if not path:
                    print(f"Unable to find a weight to connect edge {start} -> {end}")
                    if inplace:
                        return
                    return self
                else:
                    weight = search_graph.path_weight(path)

        if inplace:
            self._edges.add(WeightedDirectedEdge(start, end, weight, self.group))
            return

        return_graph = WeightedDirectedGraph(
            nodes=self._nodes,
            edges=self._edges | {WeightedDirectedEdge(start, end, weight)},
            group=self.group,
        )
        return return_graph

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

    def path_weight(
        self, path: list[str], default_value: "Group.element" = None
    ) -> "Group.element":
        """Returns the weight of following the given path in the graph"""
        if not path:
            return default_value

        if len(path) == 1:
            return self.group.identity

        uknown_nodes = set(path) - self.nodes
        if uknown_nodes:
            raise NodeNotFound(uknown_nodes)
        path_pairs = list(zip(path, path[1:]))
        path_edges_weights = [
            edge._weight for edge in self.edges if (edge.start, edge.end) in path_pairs
        ]
        if len(path_pairs) != len(path_edges_weights):
            raise ValueError(f"The path {path} is not a valid path in the graph")

        result_weight = reduce(
            self.group.operation, path_edges_weights, self.group.identity  # type: ignore
        )
        return result_weight

    def weight_between(
        self, start: str, end: str, default: "Group.element" = None
    ) -> "Group.element":
        """Returns the weight of the shortest path between two nodes."""
        path = self.find_path(start, end)
        return self.path_weight(path, default)

    @classmethod
    def from_dict(
        cls, dict: dict[str, dict[str, "Group.element"]], group: Group = _default_group
    ) -> "WeightedDirectedGraph":
        """Creates a graph from a dictionary."""
        nodes = set(dict.keys())
        edges = {
            WeightedDirectedEdge(start, end, weight, group)
            for start, end_dict in dict.items()
            for end, weight in end_dict.items()
        }
        return cls(nodes, edges, group)

    def __repr__(self) -> str:
        nodes_str = f"Nodes: {self.nodes}\n"
        edges_str = f"Edges:\n"
        for edge in self.edges:
            edges_str += f"{edge}\n"
        return nodes_str + edges_str

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
