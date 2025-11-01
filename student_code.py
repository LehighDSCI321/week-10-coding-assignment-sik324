from collections import deque


class SortableDigraph:
    def __init__(self):
        self.graph = {}

    def add_node(self, v):
        """Add node if it doesn't exist."""
        if not isinstance(v, str):
            raise TypeError("Node must be a string.")
        if v not in self.graph:
            self.graph[v] = set()

    def add_edge(self, u, v):
        """Add edge u → v."""
        self.add_node(u)
        self.add_node(v)
        self.graph[u].add(v)

    def get_children(self, node):
        """Return children of a node."""
        return self.graph.get(node, set())

    def successors(self, node):
        """Return all nodes directly reachable from the given node."""
        return self.graph.get(node, set())

    def predecessors(self, node):
        """Return all nodes that have edges leading to the given node."""
        return {u for u, nbrs in self.graph.items() if node in nbrs}

    def top_sort(self):
        """Perform topological sorting of the graph."""
        G = self.graph  # Use inherited graph
        count = dict((u, 0) for u in G)
        for u in G:
            for v in G[u]:
                count[v] += 1
        Q = [u for u in G if count[u] == 0]
        S = []
        while Q:
            u = Q.pop()
            S.append(u)
            for v in G[u]:
                count[v] -= 1
                if count[v] == 0:
                    Q.append(v)
        return S

    def __repr__(self):
        return f"{self.graph}"


class TraversableDigraph(SortableDigraph):
    def dfs(self, s):
        """Depth-First Search traversal."""
        G = self.graph
        S, Q = set(), [s]
        while Q:
            u = Q.pop()
            if u in S:
                continue
            S.add(u)
            yield u
            Q.extend(G[u])

    def bfs(self, start):
        """Breadth-First Search traversal using deque."""
        G = self.graph
        S = set()
        Q = deque([start])
        while Q:
            u = Q.popleft()
            if u in S:
                continue
            S.add(u)
            yield u
            for v in G[u]:
                Q.append(v)


class DAG(TraversableDigraph):
    def add_edge(self, u, v):
        """Add edge u → v only if it doesn’t create a cycle."""
        if self.path_exists(v, u):
            raise ValueError(f"Adding edge {u} → {v} would create a cycle.")
        super().add_edge(u, v)

    def path_exists(self, start, target):
        """Check if there is a path from start to target using DFS."""
        G = self.graph
        visited = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node == target:
                return True
            if node not in visited:
                visited.add(node)
                stack.extend(G[node])
        return False
