from ._edges import Edge, DirectedEdge, WeightedDirectedEdge, WeightedEdge


def _check_nodes_in_edges(
    nodes: set[str],
    edges: (
        set[Edge] | set[DirectedEdge] | set[WeightedDirectedEdge] | set[WeightedEdge]
    ),
) -> bool:
    edge_nodes = set().union(*[n.nodes for n in edges])
    return edge_nodes <= nodes 
