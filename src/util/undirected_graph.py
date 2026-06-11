from dataclasses import dataclass, field

@dataclass
class UndirectedGraph[T]:
    """
    A graph structure to represent an undirected graph.
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

    def add_edge(self, node1: T, node2: T) -> None:
        """
        Adds an edge between two nodes.
        If either of the nodes is not present in the graph, then it will be added.
        """
        if not self.has_node(node1):
            self.add_node(node1)
        if not self.has_node(node2):
            self.add_node(node2)
        self._adj_matrix[node1] |= set([node2])
        self._adj_matrix[node2] |= set([node1])

    def has_edge(self, node1: T, node2: T) -> bool:
        """
        Returns True if the graph has an edge between the two nodes, False otherwise
        """
        return self.has_node(node1) and node2 in self._adj_matrix[node1]

    def nodes(self) -> set[T]:
        """
        Returns the set of nodes present in the graph.
        """
        return set(self._adj_matrix.keys())

    def neighbors(self, node: T) -> set[T]:
        """
        Returns the set of neighbors of the given node.
        If the node is not present in the graph, then the empty set is returned.
        """
        if not self.has_node(node):
            return set()
        return self._adj_matrix[node]

    def __str__(self) -> str:
        out: list[str] = []
        for node, nodes in self._adj_matrix.items():
            out += [f"{node}: {{{",".join([f"{node}" for node in nodes])}}}"]
        return "\n".join(out)
