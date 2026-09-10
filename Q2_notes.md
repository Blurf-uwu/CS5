# CS5 Quarter 2 Study Notes: Linear Data Structures, Searching & Sorting

---

## 1. Memory Models & Abstract Data Types (ADTs)

- **ADT (Abstract Data Type)**: A high-level mathematical specification of a data structure defining *what* operations are supported and their operational contracts (e.g., Stack ADT requires `push`, `pop`, `peek`), independent of implementation.
- **Data Structure**: The concrete physical implementation (e.g., implementing a Stack using a static array vs a singly linked list).
- **Contiguous Memory (Arrays)**: Elements are stored in adjacent memory addresses. 
  - Allows $O(1)$ random indexing via address formula: $\text{Address}(A[i]) = \text{Base} + i \times \text{element\_size}$.
  - Resizing requires allocating a new memory block and copying all elements ($O(n)$).
- **Non-Contiguous Memory (Linked Nodes)**: Elements (nodes) are allocated arbitrarily in the heap and chained via pointer references.

---

## 2. The Stack ADT (Last-In, First-Out — LIFO)

### 2.1 Core Operations & Complexities
- `push(item)`: Insert an element onto the top of the stack — $O(1)$.
- `pop()`: Remove and return the top element — $O(1)$. (Raises error if empty).
- `peek()` / `top()`: Return the top element without removing it — $O(1)$.
- `is_empty()`: Check if stack has 0 elements — $O(1)$.
- `size()`: Return number of elements — $O(1)$.

### 2.2 Python Custom Implementation
```python
class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)
```

### 2.3 Classic Stack Application: Balanced Parentheses Check
```python
def is_balanced(expression: str) -> bool:
    stack = Stack()
    mapping = {')': '(', '}': '{', ']': '['}
    for char in expression:
        if char in mapping.values():
            stack.push(char)
        elif char in mapping.keys():
            if stack.is_empty() or stack.pop() != mapping[char]:
                return False
    return stack.is_empty()
```

---

## 3. The Queue ADT (First-In, First-Out — FIFO)

### 3.1 Why Naive Python Lists Make Inefficient Queues
- `list.pop(0)` takes $O(n)$ time because every subsequent element in memory must be shifted one slot to the left.
- **Solution 1**: Circular Queue with fixed capacity array using modulo arithmetic.
- **Solution 2**: `collections.deque` (Double-ended queue implemented as a doubly linked block list, achieving $O(1)$ appends and pops on both ends).

### 3.2 Circular Queue Implementation
```python
class CircularQueue:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0
        self.rear = 0
        self.count = 0

    def enqueue(self, item) -> bool:
        if self.is_full():
            raise OverflowError("Queue is full")
        self.queue[self.rear] = item
        self.rear = (self.rear + 1) % self.capacity
        self.count += 1
        return True

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        item = self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.count -= 1
        return item

    def is_empty(self) -> bool:
        return self.count == 0

    def is_full(self) -> bool:
        return self.count == self.capacity
```

---

## 4. Linked Lists: Singly & Doubly Linked

### 4.1 Node Definition & Singly Linked List
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def prepend(self, data):
        """Insert at beginning: O(1)"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def append(self, data):
        """Insert at end: O(n) without tail pointer, O(1) with tail"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def delete_value(self, key):
        """Delete first occurrence of key: O(n)"""
        curr = self.head
        prev = None
        while curr and curr.data != key:
            prev = curr
            curr = curr.next
        if curr is None:
            return  # Key not found
        if prev is None:
            self.head = curr.next
        else:
            prev.next = curr.next

    def reverse(self):
        """In-place reversal: O(n) time, O(1) space"""
        prev = None
        curr = self.head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev
```

### 4.2 Doubly Linked List Node Structure
```python
class DNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
```
- Allows bidirectional traversal (`curr = curr.prev` and `curr = curr.next`).
- Deletion of a given node reference is $O(1)$ because `node.prev.next = node.next` and `node.next.prev = node.prev`.

---

## 5. Search Algorithms

### 5.1 Linear Search vs Binary Search
- **Linear Search**: Checks every element sequentially.
  - Requirement: None (works on unsorted data).
  - Time Complexity: Best $O(1)$, Worst $O(n)$, Average $O(n)$.
- **Binary Search**: Repeatedly halves the search space.
  - **Precondition: Data MUST be sorted!**
  - Time Complexity: Best $O(1)$, Worst $O(\log n)$, Average $O(\log n)$.

```python
def binary_search(arr: list, target: int) -> int:
    """Returns index of target if found, else -1."""
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

---

## 6. Sorting Algorithms

### 6.1 Comparison Summary Table

| Algorithm | Best Time | Average Time | Worst Time | Space | Stable? | Key Mechanism |
|---|---|---|---|---|---|---|
| **Bubble Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes | Adjacent swaps; optimized with flag |
| **Selection Sort** | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | No | Find minimum, swap to current index |
| **Insertion Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes | Shift larger elements to insert into sorted prefix |
| **Merge Sort** | $O(n \log n)$| $O(n \log n)$| $O(n \log n)$| $O(n)$ | Yes | Divide in halves, sort, merge sorted sublists |
| **Quick Sort** | $O(n \log n)$| $O(n \log n)$| $O(n^2)$ | $O(\log n)$| No | Partition around pivot, sort left and right |

### 6.2 Merge Sort Implementation
```python
def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left: list, right: list) -> list:
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= ensures stability!
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
```

### 6.3 Quick Sort (In-Place with Lomuto Partitioning)
```python
def quicksort(arr: list, low: int, high: int):
    if low < high:
        pivot_idx = partition(arr, low, high)
        quicksort(arr, low, pivot_idx - 1)
        quicksort(arr, pivot_idx + 1, high)

def partition(arr: list, low: int, high: int) -> int:
    pivot = arr[high]  # Choosing last element as pivot
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```
