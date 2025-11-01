from collections import deque


class SortableDigraph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        """Add a directed edge u -> v"""
        if u not in self.graph:
            self.graph[u] = set()
        if v not in self.graph:
            self.graph[v] = set()
        self.graph[u].add(v)

    def get_children(self, node):
        """Return children of a node"""
        return self.graph.get(node, set())

    def __repr__(self):
        return f"{self.graph}"


class TraversableDigraph(SortableDigraph):
    def dfs(self, start, visited=None):
        """Depth-First Search traversal (recursive generator)."""
        if visited is None:
            visited = set()
        visited.add(start)
        yield start
        for neighbor in self.get_children(start):
            if neighbor not in visited:
                yield from self.dfs(neighbor, visited)

    def bfs(self, start):
        """Breadth-First Search traversal using deque (yields nodes)."""
        visited = set()
        queue = deque([start])
        visited.add(start)
        while queue:
            node = queue.popleft()
            yield node
            for neighbor in self.get_children(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)


class DAG(TraversableDigraph):
    def add_edge(self, u, v):
        """Add edge u -> v only if it doesn’t create a cycle."""
        # Check if v can reach u (which would create a cycle)
        if self._path_exists(v, u):
            raise ValueError(f"Adding edge {u} -> {v} would create a cycle.")
        super().add_edge(u, v)

    def _path_exists(self, start, target):
        """Check if there’s a path from start → target using DFS."""
        visited = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node == target:
                return True
            if node not in visited:
                visited.add(node)
                stack.extend(self.get_children(node))
        return False
