# CS5 Quarter 4 Study Notes: Graphs & Network Algorithms

---

## 1. Graph Fundamentals & Terminology

A **Graph** $G = (V, E)$ consists of:
- A set of **Vertices (Nodes)** $V$.
- A set of **Edges (Links)** $E$ connecting pairs of vertices.

### 1.1 Core Classifications
- **Undirected Graph**: Edges are bidirectional pairs $(u, v) = (v, u)$. (e.g., Two-way friendship).
- **Directed Graph (Digraph)**: Edges have a strict direction $(u \to v \neq v \to u)$. (e.g., Twitter followers, web hyperlinks).
- **Weighted Graph**: Each edge has an associated numerical cost/distance weight $w(u, v)$.
- **Degree**:
  - Undirected: Number of incident edges on vertex $v$.
  - Directed: **In-degree** (incoming edges) vs **Out-degree** (outgoing edges).
- **Path**: A sequence of vertices where each consecutive pair is connected by an edge.
- **Cycle**: A path starting and ending at the exact same vertex with at least 1 edge.
- **Connected Graph (Undirected)**: Every pair of vertices has a path connecting them.
- **Strongly Connected (Directed)**: For every pair $u, v$, there is a directed path from $u$ to $v$ AND from $v$ to $u$.

---

## 2. Graph Representations

### 2.1 Adjacency Matrix
A 2D array `matrix[V][V]` where `matrix[u][v] = 1` (or edge weight $w$) if an edge exists, else `0` (or $\infty$).
- **Space Complexity**: $\mathcal{O}(V^2)$
- **Edge Existence Check (`has_edge(u, v)`)**: $\mathcal{O}(1)$
- **Iterate Neighbors of `u`**: $\mathcal{O}(V)$
- **Best Suited For**: Dense graphs where $|E| \approx |V|^2$.

### 2.2 Adjacency List
A dictionary or array of lists where each vertex maps to a list of its outgoing neighbors.
- **Space Complexity**: $\mathcal{O}(V + E)$
- **Edge Existence Check (`has_edge(u, v)`)**: $\mathcal{O}(\text{degree}(u))$
- **Iterate Neighbors of `u`**: $\mathcal{O}(\text{degree}(u))$
- **Best Suited For**: Sparse graphs where $|E| \ll |V|^2$ (almost all real-world networks).

```python
# Python Adjacency List using standard dictionary:
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('D', 5)],
    'C': [('A', 2), ('D', 1)],
    'D': [('B', 5), ('C', 1)]
}
```

---

## 3. Graph Traversals: BFS & DFS

### 3.1 Breadth-First Search (BFS)
Explores vertices in concentric layers outward from a start node using a **Queue**.
- **Key Property**: Finds the **shortest path in unweighted graphs** (fewest edges).
- **Time Complexity**: $\mathcal{O}(V + E)$
- **Space Complexity**: $\mathcal{O}(V)$ for queue and visited set.

```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    order = []

    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order
```

### 3.2 Depth-First Search (DFS)
Explores as deep as possible along each branch before backtracking using **Recursion** (or an explicit Stack).
- **Key Property**: Detecting cycles, finding connected components, topological sorting.
- **Time Complexity**: $\mathcal{O}(V + E)$
- **Space Complexity**: $\mathcal{O}(V)$ for recursion call stack.

```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    print(start, end=" ")
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

---

## 4. Directed Acyclic Graphs (DAGs) & Topological Sort

A **DAG** is a directed graph containing **no directed cycles**.
A **Topological Sort** is a linear ordering of vertices such that for every directed edge $u \to v$, $u$ appears before $v$ in the ordering.

### 4.1 Kahn's Algorithm (In-Degree BFS Approach)
1. Compute in-degree for every vertex.
2. Enqueue all vertices with in-degree $= 0$.
3. While queue is not empty:
   - Dequeue vertex $u$, append to result list.
   - For each neighbor $v$ of $u$, decrement in-degree of $v$.
   - If in-degree of $v$ becomes 0, enqueue $v$.
4. If result list length $< V$, a cycle exists!

---

## 5. Single-Source Shortest Path: Dijkstra’s Algorithm

Finds the shortest distance from a start vertex to all other vertices in a **non-negative weighted graph**.

- **Greedy Strategy**: Always finalize the unvisited vertex with the minimum known tentative distance.
- **Data Structure**: Min-Priority Queue (`heapq`).
- **Time Complexity**: $\mathcal{O}((V + E) \log V)$ with binary heap.
- **Note**: Does NOT work with negative edge weights (requires Bellman-Ford).

```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]  # (distance, node)
    predecessors = {node: None for node in graph}

    while pq:
        curr_dist, u = heapq.heappop(pq)

        if curr_dist > distances[u]:
            continue  # Outdated entry in heap

        for v, weight in graph[u]:
            distance = curr_dist + weight
            # Relaxation step:
            if distance < distances[v]:
                distances[v] = distance
                predecessors[v] = u
                heapq.heappush(pq, (distance, v))

    return distances, predecessors
```

---

## 6. Minimum Spanning Trees (MST)

For a connected, undirected, weighted graph:
- A **Spanning Tree** connects all $|V|$ vertices using exactly $|V| - 1$ edges with no cycles.
- A **Minimum Spanning Tree** minimizes the total sum of edge weights.

### 6.1 Kruskal’s Algorithm (Edge-Centric)
1. Sort all edges in non-decreasing order of weight.
2. Initialize Disjoint-Set (Union-Find) structure where each vertex is its own set.
3. Iterate through sorted edges: if endpoints $u$ and $v$ belong to different sets, add edge to MST and union their sets; otherwise skip (to avoid cycle).
- **Time Complexity**: $\mathcal{O}(E \log E)$

### 6.2 Prim’s Algorithm (Vertex-Centric)
1. Start from an arbitrary node; add it to the visited set.
2. Maintain a priority queue of all edges leaving the currently visited set.
3. Repeatedly extract the minimum weight edge that connects to an unvisited vertex.
- **Time Complexity**: $\mathcal{O}((V + E) \log V)$
