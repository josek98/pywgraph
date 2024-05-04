from ._edges import Edge, DirectedEdge, WeightedDirectedEdge, WeightedEdge
from ._graph_utils import _check_nodes_in_edges


class Graph:

    def __init__(self, nodes: set[str], edges: set[Edge]) -> None:
        if not _check_nodes_in_edges(nodes, edges):
            raise ValueError("Nodes of edges must be in set of nodes")
        
        self._nodes = nodes 
        self._edges = edges

    @property
    def nodes(self) -> set[str]:
        return self._nodes
    
    @property
    def edges(self) -> set[Edge]:
        return self._edges
    
