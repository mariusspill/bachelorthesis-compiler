from collections import deque
from dataclasses import dataclass, field
from typing import Iterator

@dataclass
class DirectedGraph[T]:
    """
    A graph structure to represent a directed graph.
    """

    # maps nodes to its set of neighbors
    _adj_matrix: dict[T, set[T]] = field(default_factory=lambda: {})

    def add_node(self, node: T) -> None:
        """
        Adds an node to the graph.
        If the node is already present in the graph, then the function returns without any action.
        """
        if node in self._adj_matrix:
            return
        self._adj_matrix[node] = set()

    def has_node(self, node: T) -> bool:
        """
        Returns True if the node is already present in the graph, False otherwise
        """
        return node in self._adj_matrix

    def add_edge(self, source: T, target: T) -> None:
        """
        Adds an edge between from source to target.
        If either of the nodes is not present in the graph, then it will be added.
        """
        if not self.has_node(source):
            self.add_node(source)
        if not self.has_node(target):
            self.add_node(target)
        self._adj_matrix[source] |= set([target])

    def has_edge(self, source: T, target: T) -> bool:
        """
        Returns True if the graph has an edge between the two nodes, False otherwise
        """
        return self.has_node(source) and target in self._adj_matrix[source]

    def nodes(self) -> set[T]:
        """
        Returns the set of nodes present in the graph.
        """
        return set(self._adj_matrix.keys())

    def neighbors_in(self, node: T) -> set[T]:
        """
        Returns the set of neighbors of the given node.
        If the node is not present in the graph, then the empty set is returned.
        """
        ns: set[T] = set()
        for src, tgts in self._adj_matrix.items():
            if node in tgts:
                ns.add(src)
        return ns

    def neighbors_out(self, node: T) -> set[T]:
        """
        Returns the set of neighbors of the given node.
        If the node is not present in the graph, then the empty set is returned.
        """
        if not self.has_node(node):
            return set()
        return self._adj_matrix[node].copy()

    def transpose(self) -> 'DirectedGraph[T]':
        """
        Transposes the graph inplace in place.
        Returns `self` for better ergonomics with method chaining.
        """
        adj_matrix: dict[T, set[T]] = {}
        for source, targets in self._adj_matrix.items():
            if source not in adj_matrix:
                adj_matrix[source] = set()
            for target in targets:
                if target not in adj_matrix:
                    adj_matrix[target] = set()
                adj_matrix[target] |= {source}
        self._adj_matrix = adj_matrix
        return self

    def iter_topological(self) -> Iterator[T]:
        """
        Iterates the nodes of the graph in topological order.
        Assumes the graph to be acyclic.
        """
        in_degrees = {node: 0 for node in self.nodes()}
        for targets in self._adj_matrix.values():
            for target in targets:
                in_degrees[target] += 1

        queue: deque[T] = deque()

        for node in self.nodes():
            if in_degrees[node] == 0:
                queue.append(node)

        while queue:
            node = queue.pop()
            yield node

            for neighbor in self.neighbors_out(node):
                in_degrees[neighbor] -= 1
                if in_degrees[neighbor] == 0:
                    queue.append(neighbor)

    def __str__(self) -> str:
        out: list[str] = []
        for node, nodes in self._adj_matrix.items():
            out += [f"{node}: {{{",".join([f"{node}" for node in nodes])}}}"]
        return "\n".join(out)
