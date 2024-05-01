class NodeNotFound(Exception):
    """Exception raised when a node is not found in a graph."""

    def __init__(self, node: str) -> None:
        self.node = node
        super().__init__(f"Node '{node}' not found in the graph.")
