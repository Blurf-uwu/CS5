# CS5 Quarter 1 Study Notes: Python Review & Project Management

---

## 1. Professional Development & Project Management

### 1.1 Software Development Life Cycle (SDLC) & Agile
- **Waterfall vs Agile**: Waterfall is sequential and rigid; Agile is iterative, welcoming feedback and incremental improvements in 1-to-2 week **sprints**.
- **User Story Format**: 
  > *"As a [role], I want to [action/feature] so that [business value/benefit]."*
- **Acceptance Criteria**: Concrete conditions that must be satisfied for a story to be marked as "Done" (often tested with automated test cases).

### 1.2 Git Version Control Fundamentals
```bash
git init                   # Initialize a new repository
git status                 # Inspect unstaged/staged files
git add <file>             # Stage specific file (or 'git add .' for all)
git commit -m "feat: msg"  # Commit with standard semantic message
git branch -M main         # Rename default branch to main
git log --oneline --graph  # View visual commit tree
```

---

## 2. Variables, Memory References & Primitive Types

### 2.1 Everything is an Object
In Python, variables do not store raw values directly; they store **references (memory addresses)** to objects in memory.

```python
x = 256
y = 256
print(x is y)      # True (small integer caching in CPython)

a = 1000
b = 1000
print(a == b)      # True (value equality)
print(a is b)      # False (distinct memory objects, id(a) != id(b))
```

### 2.2 Primitive Types & Conversions
- `int`: Arbitrary-precision signed integers (no 32-bit/64-bit overflow in Python 3).
- `float`: 64-bit double-precision IEEE 754 floating point numbers.
- `bool`: Subclass of `int` (`True == 1`, `False == 0`).
- `str`: Immutable sequence of Unicode characters.

```python
# Truncation vs Rounding:
int(4.9)         # -> 4 (truncates towards zero)
round(4.5)       # -> 4 (banker's rounding: rounds to nearest EVEN number)
round(5.5)       # -> 6
round(3.14159, 2)# -> 3.14
```

---

## 3. Formatted I/O & String Operations

### 3.1 `input()` Sanitization
`input()` always captures user input as a `str`. To prevent unexpected crashes, combine it with string cleaning methods:

| String Method | Result on `"  Admin_User \n"` | Description |
|---|---|---|
| `.strip()` | `"Admin_User"` | Trims leading and trailing whitespace/newlines |
| `.lower()` | `"  admin_user \n"` | Converts all characters to lowercase |
| `.upper()` | `"  ADMIN_USER \n"` | Converts all characters to uppercase |
| `.capitalize()`| `"  admin_user \n"` (or `"Admin"` if stripped) | Capitalizes first character |
| `.title()` | `"  Admin_User \n"` | Capitalizes every word |

### 3.2 F-String Formatting Cheatsheet
```python
price = 142.5
qty = 3
discount = 0.15
total = price * qty * (1 - discount)

print(f"Item Total: Php {total:,.2f}")   # Item Total: Php 363.38
print(f"Discount Rate: {discount:.1%}")  # Discount Rate: 15.0%
print(f"Padded Order ID: {qty:05d}")    # Padded Order ID: 00003
print(f"Alignment: {'LEFT':<10} | {'RIGHT':>10}")
```

---

## 4. Operators & Evaluation Mechanics

### 4.1 Short-Circuit Evaluation
Logical operators `and` and `or` evaluate from left to right and stop as soon as the outcome is deterministic.

```python
# Safe division: if divisor is 0, second condition is never evaluated!
if divisor != 0 and (numerator / divisor) > 2.0:
    print("Valid ratio")

# Default fallback pattern:
user_name = input_name or "Anonymous"
```

### 4.2 Chained Comparisons
Python evaluates `a < b < c` as `(a < b) and (b < c)` without evaluating `b` twice.
```python
weight = 7.5
if 0 <= weight <= 10:
    print("Standard weight class")
```

---

## 5. Defensive Programming & Control Structures

### 5.1 Robust Input Validation Loops
Never trust raw user input. Use an infinite `while True` loop with `try-except` to enforce validation invariants:

```python
def get_positive_float(prompt: str) -> float:
    """Repeatedly prompts until user provides a non-negative float."""
    while True:
        raw = input(prompt).strip()
        try:
            val = float(raw)
            if val < 0:
                print("Error: Value cannot be negative. Please try again.")
                continue
            return val
        except ValueError:
            print(f"Error: '{raw}' is not a valid decimal number. Try again.")
```

### 5.2 Loop `else` Clause
A loop's `else` block executes **only if the loop completed naturally** (without hitting a `break`).

```python
target = 42
numbers = [10, 20, 30, 42, 50]

for n in numbers:
    if n == target:
        print(f"Found {target}!")
        break
else:
    print(f"{target} is not in the list.")
```

---

## 6. Functions & Scope Resolution

### 6.1 Function Signatures & Argument Types
```python
def calculate_shipping(
    weight: float, 
    destination: str = "Domestic", 
    *surcharges: float, 
    **metadata
) -> float:
    """
    Computes total shipping cost.
    - weight: package mass in kg
    - destination: 'Domestic' or 'International'
    - *surcharges: optional variable positional fees
    - **metadata: optional key-value pairs (e.g., courier='LBC')
    """
    base_rate = 50.0 if destination == "Domestic" else 200.0
    variable_rate = weight * (15.0 if destination == "Domestic" else 45.0)
    extra_fees = sum(surcharges)
    return base_rate + variable_rate + extra_fees
```

### 6.2 The LEGB Scope Rule
Python resolves variable identifiers in this exact order:
1. **L**ocal: Inside the current function.
2. **E**nclosing: In any enclosing nested functions (`nonlocal`).
3. **G**lobal: Defined at top-level module (`global`).
4. **B**uilt-in: Reserved namespace (`len`, `range`, `print`, `ValueError`).

> **Rule of Thumb:** Avoid using the `global` keyword. Pass values as arguments and return results.

---

## 7. Complex Built-In Collections

| Type | Syntax | Mutable? | Ordered? | Lookup Time | Best Use Case |
|---|---|---|---|---|---|
| **`list`** | `[1, 2, 3]` | Yes | Yes | $O(n)$ search, $O(1)$ append | Sequential items, dynamic queues |
| **`tuple`** | `(1, "A", True)`| No | Yes | $O(n)$ search | Fixed records, dictionary keys |
| **`dict`** | `{"id": 101}` | Yes | Yes (Python 3.7+) | $O(1)$ average | Key-value mapping, database records |
| **`set`** | `{1, 2, 3}` | Yes | No | $O(1)$ average | Uniqueness, membership test, set math |

### 7.1 Powerful Dictionary & Comprehension Idioms
```python
# Dictionary lookup with safe fallback:
menu = {"Coffee": 120.0, "Tea": 90.0}
price = menu.get("Matcha", 100.0)  # Returns default 100.0 if key absent

# List and Dict Comprehensions:
discounted_prices = {item: price * 0.9 for item, price in menu.items()}
heavy_packages = [pkg for pkg in [3.2, 11.5, 8.1, 14.0] if pkg > 10.0]
```
