from collections import deque


class SortableDigraph:
    """A directed graph with sortable and traversal functionality."""

    def __init__(self):
        """Initialize an empty directed graph."""
        self.graph = {}

    def add_node(self, node_name):
        """Add a node if it doesn't exist."""
        if not isinstance(node_name, str):
            raise TypeError("Node name must be a string.")
        if node_name not in self.graph:
            self.graph[node_name] = {}

    def get_nodes(self):
        """Return all nodes in the graph."""
        return list(self.graph.keys())

    def add_edge(self, source, target, edge_weight=None):
        """Add a directed edge source → target with optional weight."""
        self.add_node(source)
        self.add_node(target)
        self.graph[source][target] = edge_weight

    def get_children(self, node_name):
        """Return children of a node."""
        return list(self.graph.get(node_name, {}).keys())

    def successors(self, node_name):
        """Return all nodes directly reachable from the given node."""
        return sorted(list(self.graph.get(node_name, {}).keys()))

    def predecessors(self, node_name):
        """Return all nodes that have edges leading to the given node."""
        return sorted(
            [src for src, neighbors in self.graph.items() if node_name in neighbors]
        )

    def top_sort(self):
        """Perform topological sorting of the graph."""
        in_degree = {u: 0 for u in self.graph}
        for _, neighbors in self.graph.items():
            for vertex in neighbors:
                in_degree[vertex] += 1

        queue = [u for u in self.graph if in_degree[u] == 0]
        sorted_nodes = []

        while queue:
            node = queue.pop()
            sorted_nodes.append(node)
            for neighbor in self.graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return sorted_nodes

    def __repr__(self):
        """Return string representation of the graph."""
        return f"{self.graph}"


class TraversableDigraph(SortableDigraph):
    """A digraph that supports traversal algorithms."""

    def dfs(self, start_node):
        """Depth-First Search traversal."""
        visited = set()
        stack = [start_node]

        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            yield node
            stack.extend(self.graph[node].keys())

    def bfs(self, start_node):
        """Breadth-First Search traversal using deque."""
        visited = set()
        queue = deque([start_node])

        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            yield node
            for neighbor in self.graph[node].keys():
                queue.append(neighbor)


class DAG(TraversableDigraph):
    """A Directed Acyclic Graph that prevents cycle creation."""

    def add_edge(self, source, target, edge_weight=None):
        """Add edge source → target only if it doesn’t create a cycle."""
        if self.path_exists(target, source):
            raise ValueError(
                f"Adding edge {source} → {target} would create a cycle."
            )
        super().add_edge(source, target, edge_weight=edge_weight)

    def path_exists(self, start_node, target_node):
        """Check if there is a path from start_node to target_node using DFS."""
        if start_node not in self.graph:
            return False

        visited = set()
        stack = [start_node]

        while stack:
            node = stack.pop()
            if node == target_node:
                return True
            if node not in visited:
                visited.add(node)
                stack.extend(self.graph.get(node, {}).keys())
        return False
