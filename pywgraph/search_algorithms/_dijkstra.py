from typing import Any, NamedTuple
from ..graphs import Path, WeightedDirectedGraph
from ..groups import Group

class DijkstraResult(NamedTuple):
    path: Path
    weight: "Group.element" # type: ignore


class Dijkstra:

    def __init__(self, graph: WeightedDirectedGraph, start: str):
        self._graph = graph
        self._start = start
        self._table = self._initial_dijkstra_table
        self._executed = False

    @property
    def graph(self) -> WeightedDirectedGraph:
        return self._graph

    @property
    def start(self) -> str:
        return self._start

    @property
    def table(self) -> dict[str, dict[str, "Group.element"]]:
        return self._table

    @property
    def _initial_dijkstra_table(self) -> dict[str, dict[str, Any]]:
        """{node: {"ShortestWeight": weight, "PreviousNode": node}}"""

        table: dict[str, dict[str, Any]] = {node: {} for node in self.graph.nodes}
        table[self.start] = {"ShortestWeight": self.graph.group.identity}
        return table

    def perform_dijkstra_algorithm(self) -> None:

        if self._executed:
            return

        table: dict[str, dict[str, "Group.element"]] = self._initial_dijkstra_table
        visited: set[str] = set()
        unvisited = self.graph.nodes.copy()
        next_node = self.start

        while next_node:

            self._dijkstra_iter(
                graph=self.graph,
                node=next_node,
                visited=visited,
                unvisited=unvisited,
                table=table,
            )

            next_node = self._next_node(
                table=table,
                unvisited=unvisited,
                group=self.graph.group,
                start=next_node, # type: ignore
            )

        self._table = table
        self._executed = True

    def shortest_path(
        self, start: str, end: str,
    ) -> DijkstraResult:
        """Returns the shortest path from start to end in the table."""

        if not self._executed:
            self.perform_dijkstra_algorithm()

        path = Path([end])
        current_node = end
        while current_node != start:
            current_node = self.table[current_node]["PreviousNode"]
            path.append(current_node)

        path = Path(path[::-1])
        weight = self.graph.path_weight(path)
        return DijkstraResult(path, weight)

    # region: auxiliary methods
    @classmethod
    def _dijkstra_iter(
        cls,
        graph: WeightedDirectedGraph,
        node: str,
        visited: set[str],
        unvisited: set[str],
        table: dict[str, dict[str, "Group.element"]],
    ):
        """Updates visit and unvisited nodes and the dijkstra table."""

        visited.add(node)
        unvisited.remove(node)
        current_weight = table[node]["ShortestWeight"]

        unvisited_children = {
            (child, child_weight)
            for child, child_weight in graph.children_with_weight(node)
            if child not in visited
        }
        for child, child_weight in unvisited_children:

            child_current_weight = table[child].get("ShortestWeight")
            extended_weight = graph.group(current_weight, child_weight)

            if child_current_weight is None:
                table[child]["ShortestWeight"] = extended_weight
                table[child]["PreviousNode"] = node
            elif graph.group.le(extended_weight, child_current_weight):
                table[child]["ShortestWeight"] = extended_weight
                table[child]["PreviousNode"] = node

    @classmethod
    def _next_node(
        cls,
        table: dict[str, dict[str, Any]],
        unvisited: set[str],
        group: Group,
        start: str,
    ) -> str | None:
        if not unvisited:
            return None

        _filter_table = {
            key: value.get("ShortestWeight")
            for key, value in table.items()
            if ((value.get("ShortestWeight") is not None) and (key in unvisited))
        }
        if not _filter_table:
            return start
        _min_weight = min(_filter_table.values(), key=group.cmp_key)
        _next_node = [
            key for key, value in _filter_table.items() if value == _min_weight
        ][0]
        return _next_node