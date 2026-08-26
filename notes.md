# Python Notes — CS5

---

## 1. `input()` — Getting User Input

Always returns a **string**. You must convert it if you need a number.

```python
name = input("Enter your name: ")   # string
age  = int(input("Enter age: "))    # convert to int
temp = float(input("Temperature: ")) # convert to float
```

**Useful string methods on input:**

| Method | What it does | Example |
|---|---|---|
| `.lower()` | all lowercase | `"END".lower()` → `"end"` |
| `.upper()` | all uppercase | `"yes".upper()` → `"YES"` |
| `.capitalize()` | first letter upper | `"domestic".capitalize()` → `"Domestic"` |
| `.strip()` | removes whitespace from both ends | `" hi ".strip()` → `"hi"` |

> Used in every file — MP1, MP2, taxi meter, shipping cost.

---

## 2. `float()` and `int()` — Type Conversion

```python
float("3.14")   # → 3.14
int("5")        # → 5
int(3.9)        # → 3   (truncates, does NOT round)
```

> **Quirk:** `int()` on a float *truncates* toward zero, not rounds.
> Use `round()` to round, then `int()` if needed.

---

## 3. `print()` with f-strings — Formatted Output

```python
name = "Zy"
score = 95.678

print(f"Hello, {name}!")             # Hello, Zy!
print(f"Score: {score:.2f}")         # Score: 95.68  (2 decimal places)
print(f"Score: {score:.4f}")         # Score: 95.6780
print(f"Rounded: {round(score, 2)}") # Rounded: 95.68
```

**Format specifiers inside `{}`:**

| Specifier | Meaning | Example result |
|---|---|---|
| `:.2f` | 2 decimal places (float) | `95.68` |
| `:d` | integer | `95` |
| `:,` | thousands separator | `1,000,000` |
| `:.2%` | percentage | `0.956` → `95.60%` |

> Used in Lab1 (`:.4f`), MP1/MP2/taxi meter (`:.2f`).

---

## 4. `if / elif / else` — Conditionals

```python
x = 7
if x > 10:
    print("big")
elif x > 5:
    print("medium")   # this runs
else:
    print("small")
```

**Chained comparisons** (Python-only shortcut):
```python
# Instead of: 0 <= weight and weight <= 5
if 0 <= weight <= 5:   # cleaner Python style
    ...
```
> Used in Lab3, shipping cost files, Lab4's `in_range`.

---

## 5. `while True` loop with `break` and `continue`

```python
while True:
    answer = input("Again? (yes/no): ")
    if answer == "no":
        break       # exits the loop entirely
    if answer != "yes":
        continue    # skips the rest, restarts the loop
    print("Going again!")
```

- `break` → **stop** the loop
- `continue` → **skip** the rest of this iteration, go back to the top

> Used in MP1, MP2, MP1_v2, taxi meter, shipping cost.

---

## 6. `for` loop and `range()`

```python
for i in range(5):          # 0, 1, 2, 3, 4
for i in range(1, 6):       # 1, 2, 3, 4, 5
for i in range(0, 10, 2):   # 0, 2, 4, 6, 8   (step)
for i in range(10, 0, -1):  # 10, 9, 8, ... 1  (countdown)
```

**`range(start, stop, step)` quirks:**
- `stop` is **exclusive** (never included).
- A negative `step` counts down; `start` must be > `stop`.
- An *empty* range (e.g. `range(0, -2)` with positive step) produces nothing — the `in` check is still `False`.

```python
# Checking membership
14 in range(0, 100, 2)   # True  (14 is even, in range)
14 in range(0, 2)        # False (range is only 0, 1)
```

> Used in Lab2 (membership test), Lab3 (factorial), Lab4, MP2, taxi meter.

---

## 7. Defining Functions with `def`

```python
def greet(name):
    return f"Hello, {name}!"

result = greet("Zy")  # call the function
print(result)
```

- Everything inside the function is **indented**.
- `return` sends a value back to the caller.
- A function with no `return` gives back `None`.

---

## 8. Default Parameter Values

```python
def power(exponent, base=10):   # base defaults to 10
    return base ** exponent

power(3)        # 10 ** 3 = 1000
power(3, 2)     # 2  ** 3 = 8
```

> **Rule:** default parameters must come *after* non-default ones.
> Used in Lab4 `power()` and Lab2 `inforloop()`.

---

## 9. `*args` — Arbitrary (Variable) Arguments

```python
def sum_all(*args):      # args is a tuple of all extra arguments
    total = 0
    for num in args:
        total += num
    return total

sum_all(1, 2, 3, 4)   # → 10
sum_all(5, 10)         # → 15
```

You can mix normal and `*args` params — but `*args` must come **after** regular ones:
```python
def in_range(number, *args):   # first arg is normal, rest go into args
    ...
```
> Used in Lab4: `sum_all`, `print_evens`, `in_range`.

---

## 10. List Comprehension

A compact way to build a list:

```python
# Long way:
evens = []
for num in args:
    if num % 2 == 0:
        evens.append(num)

# Short way (list comprehension):
evens = [num for num in args if num % 2 == 0]
```

> Used in Lab4 `print_evens()`.

---

## 11. `try / except` — Handling Errors Gracefully

```python
try:
    value = float(input("Enter a number: "))
except ValueError:
    print("That's not a valid number!")
```

- `ValueError` is raised when conversion fails (e.g. `float("abc")`).
- Use `except Exception as e:` to catch *any* error and print its message.

```python
try:
    result = risky_function()
except Exception as e:
    print(f"An error occurred: {e}")   # e holds the error message
```

> Used in MP1_v2 and taxi meter for robust input handling.

---

## 12. `raise` — Manually Triggering an Error

```python
def calculate_weight_cost(weight):
    if weight < 0:
        raise ValueError(f"Unexpected weight value: {weight}")
    ...
```

Useful to signal that something impossible happened — forces the caller to handle it.

> Used in MP1_v2.

---

## 13. `round()`, `max()`, `min()`, `abs()`

```python
round(3.14159, 2)   # → 3.14
round(3.5)          # → 4  (rounds to nearest even in Python 3 — "banker's rounding")
max(3, 7, 1)        # → 7
min(3, 7, 1)        # → 1
abs(-5)             # → 5
```

> `max()` used in Lab3 `greatest_of_three()`.
> `round()` used in Lab1 windchill formula.

---

## 14. Membership Test with `in`

```python
# Check if a value is in a list/tuple/range/string
if destination in ("Domestic", "International"):
    ...

if "a" in "banana":   # True
    ...

14 in range(0, 100, 2)   # True
```

> Used in MP1_v2 and Lab2.

---

## 15. `**` — Exponentiation Operator

```python
2 ** 10    # → 1024
9 ** 0.5   # → 3.0  (square root)
v ** 0.16  # used in the windchill formula (Lab1)
```

> Also: `%` is the **modulo** (remainder) operator.
> `10 % 3` → `1`. Used in Lab3 for odd/even check.

---

## 16. `+=`, `-=`, `*=` — Augmented Assignment

```python
total = 0
total += 50    # same as: total = total + 50
total *= 1.20  # same as: total = total * 1.20
result *= i    # used in factorial loop (Lab3)
```

---

## 17. Docstrings — Documenting Functions

```python
def calculate_shipping_cost():
    """Calculates and returns the total shipping cost, or None on invalid input."""
    ...
```

- Triple-quoted string right after `def` line.
- Shown by `help(function_name)` in the Python shell.
- Good habit — always document what a function does.

> Used in shipping cost 2.py.

---

## 18. `None` — The "No Value" Value

```python
def get_weight_cost():
    ...
    return None   # signals "something went wrong"

result = get_weight_cost()
if result is None:       # always use `is None`, not `== None`
    print("Invalid!")
```

> Used throughout shipping cost 2.py as a sentinel for invalid input.

---

# Useful Stuff NOT Yet Used in the Files

---

## A. `while/else` and `for/else`

The `else` block runs only if the loop was **not** broken out of:

```python
for i in range(5):
    if i == 3:
        break
else:
    print("Loop finished without break")  # won't run here

# Useful for search loops:
for item in items:
    if item == target:
        print("Found!")
        break
else:
    print("Not found.")   # runs only if target was never found
```

---

## B. f-string Advanced Expressions

```python
# You can put any expression inside f-strings:
print(f"{ 2 ** 10 }")                          # 1024
print(f"{ 'yes' if x > 0 else 'no' }")        # inline if
print(f"{'hello':>10}")    # right-align:      "     hello"
print(f"{'hello':<10}|")   # left-align:       "hello     |"
print(f"{42:05d}")         # zero-pad:          "00042"
```

---

## C. `enumerate()` — Loop with Index and Value

```python
fruits = ["apple", "banana", "cherry"]

for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry

# Start index at 1:
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")
```

---

## D. `zip()` — Loop Over Two Lists Together

```python
names  = ["Alice", "Bob", "Carol"]
scores = [90, 85, 78]

for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

---

## E. `list`, `append()`, `len()`, and slicing

```python
nums = [1, 2, 3]
nums.append(4)       # [1, 2, 3, 4]
len(nums)            # 4
nums[0]              # 1  (first element)
nums[-1]             # 4  (last element)
nums[1:3]            # [2, 3]  (slice)
nums[::-1]           # [4, 3, 2, 1]  (reversed)
```

---

## F. `dict` — Key-Value Pairs

```python
rates = {"Domestic": 0.00, "International": 7.50}
cost = rates["International"]   # → 7.50

# Safer lookup with default:
cost = rates.get("Express", 0)  # → 0 (key doesn't exist, returns default)
```

Dictionaries can replace long `if/elif` chains:
```python
weight_cost = {
    "light":  50.00,
    "medium": 100.00,
    "heavy":  150.00,
}
```

---

## G. `lambda` — One-Line Anonymous Functions

```python
square = lambda x: x ** 2
square(5)   # → 25

# Useful with sorted():
pairs = [(1, 'b'), (3, 'a'), (2, 'c')]
pairs.sort(key=lambda pair: pair[0])   # sort by first element
```

---

## H. `assert` — Quick Sanity Checks

```python
def factorial(n):
    assert n >= 0, "n must be non-negative"
    ...
```

Raises `AssertionError` if the condition is False. Good for catching bugs during development.

---

## I. Multiple Return Values

Python functions can return multiple values as a tuple:

```python
def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([3, 1, 7, 2])
print(lo, hi)   # 1 7
```

---

## J. `math` module — Common Math Functions

```python
import math

math.sqrt(16)       # → 4.0
math.floor(3.9)     # → 3  (always rounds down)
math.ceil(3.1)      # → 4  (always rounds up)
math.pi             # → 3.141592653589793
math.factorial(5)   # → 120
math.log(100, 10)   # → 2.0  (log base 10)
```

> Alternative to `**0.5` for square roots; cleaner for complex math.
