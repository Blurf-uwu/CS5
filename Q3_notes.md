# CS5 Quarter 3 Study Notes: Algorithm Efficiency Analysis & Trees

---

## 1. Algorithm Efficiency Analysis

### 1.1 Empirical vs Theoretical Analysis
- **Empirical Analysis (Benchmarking)**:
  - Measures actual wall-clock elapsed time on physical hardware.
  - Tools: Python's `time.perf_counter()` (high-resolution timer) and `tracemalloc`.
  - Limitations: Heavily influenced by CPU speed, operating system background processes, RAM limits, and compiler/interpreter optimizations.
- **Theoretical Analysis (Asymptotic Analysis)**:
  - Evaluates algorithmic resource consumption as an abstract mathematical function of input size $n$ (independent of machine hardware).
  - Counts primitive machine instructions executed.

```python
import time

def benchmark(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    elapsed = end - start
    print(f"Executed {func.__name__} in {elapsed:.6f} seconds")
    return result
```

---

## 2. Asymptotic Notations & Big-O

### 2.1 The Big-Three Asymptotic Bounds
1. **Big-O ($\mathcal{O}$)**: Asymptotic **Upper Bound** (Worst-case performance guarantee).
   $$f(n) \in \mathcal{O}(g(n)) \iff \exists c > 0, n_0 > 0 \text{ such that } 0 \le f(n) \le c \cdot g(n) \quad \forall n \ge n_0$$
2. **Big-Omega ($\Omega$)**: Asymptotic **Lower Bound** (Best-case baseline).
   $$f(n) \in \Omega(g(n)) \iff \exists c > 0, n_0 > 0 \text{ such that } 0 \le c \cdot g(n) \le f(n) \quad \forall n \ge n_0$$
3. **Big-Theta ($\Theta$)**: Asymptotic **Tight Bound** ($f(n)$ is bounded above and below by $g(n)$).

### 2.2 Common Complexity Classes (Ordered from Fastest to Slowest)

| Notation | Name | Typical Example | Behavior as $n \to \infty$ |
|---|---|---|---|
| $\mathcal{O}(1)$ | Constant | Hash map lookup, array index access | Does not change with $n$ |
| $\mathcal{O}(\log n)$ | Logarithmic | Binary search, BST search (balanced) | Doubles input adds constant steps |
| $\mathcal{O}(n)$ | Linear | Linear search, array traversal | Direct 1:1 proportionality |
| $\mathcal{O}(n \log n)$| Linearithmic | Merge sort, Quick sort (average) | Efficient divide-and-conquer |
| $\mathcal{O}(n^2)$ | Quadratic | Bubble sort, nested pairwise loop | $10\times$ size $\to 100\times$ time |
| $\mathcal{O}(2^n)$ | Exponential | Recursive Fibonacci, power set | Rapidly becomes intractable |
| $\mathcal{O}(n!)$ | Factorial | Traveling Salesperson brute force | Impossible for $n > 20$ |

---

## 3. Tree Fundamentals & Terminology

A **Tree** is a non-linear, hierarchical data structure consisting of nodes connected by directed edges, with **no cycles**.

- **Root**: Topmost node without parent.
- **Edge**: Directed link from parent to child.
- **Parent / Child**: Direct ancestor / direct descendant.
- **Leaf (External Node)**: A node with 0 children.
- **Depth of a Node**: Number of edges on the path from root to that node ($\text{depth}(\text{root}) = 0$).
- **Height of a Node**: Number of edges on the longest downward path from node to a leaf ($\text{height}(\text{leaf}) = 0$).
- **Height of a Tree**: Height of the root node.

### 3.1 Binary Tree Classifications
- **Full Binary Tree**: Every node has either 0 or 2 children (no node has 1 child).
- **Complete Binary Tree**: All levels are completely filled except possibly the last, which is filled from left to right.
- **Perfect Binary Tree**: All internal nodes have 2 children and all leaves are at the same level. Total nodes $= 2^{h+1} - 1$.
- **Balanced Binary Tree**: For every node, the height difference between left and right subtrees is at most 1.

---

## 4. Tree Traversal Operations

Traversals visit every node in the tree exactly once.

### 4.1 Depth-First Traversals (DFS)
```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def preorder(root):
    """Root -> Left -> Right"""
    if root:
        print(root.val, end=" ")
        preorder(root.left)
        preorder(root.right)

def inorder(root):
    """Left -> Root -> Right (Yields sorted order in a BST!)"""
    if root:
        inorder(root.left)
        print(root.val, end=" ")
        inorder(root.right)

def postorder(root):
    """Left -> Right -> Root (Ideal for deleting nodes / bottom-up calculations)"""
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.val, end=" ")
```

### 4.2 Breadth-First Traversal (Level-Order using Queue)
```python
from collections import deque

def level_order(root):
    """Visits nodes level by level from top to bottom, left to right."""
    if not root:
        return
    queue = deque([root])
    while queue:
        node = queue.popleft()
        print(node.val, end=" ")
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
```

---

## 5. Binary Search Trees (BST)

### 5.1 The BST Invariant
For every node $X$:
- All keys in $X$'s left subtree must be strictly less than $X.\text{key}$.
- All keys in $X$'s right subtree must be strictly greater than $X.\text{key}$.

### 5.2 BST Search & Insert
```python
class BST:
    def __init__(self):
        self.root = None

    def search(self, key):
        curr = self.root
        while curr:
            if key == curr.val:
                return curr
            elif key < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        return None

    def insert(self, val):
        if not self.root:
            self.root = TreeNode(val)
            return
        curr = self.root
        while True:
            if val < curr.val:
                if curr.left is None:
                    curr.left = TreeNode(val)
                    break
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = TreeNode(val)
                    break
                curr = curr.right
```

### 5.3 BST Node Deletion (The 3 Cases)
1. **Case 1: Node is a Leaf (0 children)**: Simply disconnect node from parent.
2. **Case 2: Node has 1 Child**: Replace node with its single child.
3. **Case 3: Node has 2 Children**: Find the **In-order Successor** (smallest node in the right subtree), copy its value to the current node, then recursively delete the in-order successor node.

```python
def delete_node(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        # Case 1 & 2
        if not root.left:
            return root.right
        elif not root.right:
            return root.left
        # Case 3: Two children
        temp = find_min(root.right)
        root.val = temp.val
        root.right = delete_node(root.right, temp.val)
    return root

def find_min(node):
    curr = node
    while curr.left:
        curr = curr.left
    return curr
```

---

## 6. Priority Queues & Binary Heaps

A **Binary Heap** is a complete binary tree stored compactly inside an array without pointer overhead.

- **Parent Index**: $\lfloor (i - 1) / 2 \rfloor$
- **Left Child Index**: $2i + 1$
- **Right Child Index**: $2i + 2$
- **Min-Heap Property**: Parent value $\le$ Children values (Root is always absolute minimum).
- **Time Complexities**:
  - `insert`: $\mathcal{O}(\log n)$ (sift up)
  - `extract_min`: $\mathcal{O}(\log n)$ (replace root with last leaf, sift down)
  - `get_min`: $\mathcal{O}(1)$
  - `build_heap`: $\mathcal{O}(n)$
