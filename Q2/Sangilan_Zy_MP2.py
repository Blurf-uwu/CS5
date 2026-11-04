"""
This program is a model of bacterial population growth using the Fibonacci sequence:
- Hour 0: 0 bacteria (baseline)
- Hour 1: 1 bacterium (initial mature cell)
- Hour h: Population from previous hour (h - 1) + population from two hours ago (h - 2)

1. Base Case Condition:
   hours <= 1 (int)
2. Base Definition:
   Returns hours directly (0 for Hour 0, 1 for Hour 1).
3. Recursive Case Condition:
   hours > 1.
4. Recursive Definition:
   bacterial_population(hours - 1) + bacterial_population(hours - 2).
"""


def bacterial_population(hours):
    """Calculate the total bacterial population recursively after a given number of hours.

    Parameters:
        hours (int): Non-negative number of hours elapsed.

    Returns:
        int: Total bacterial population at hour h.
    """
    if hours < 0:
        raise ValueError("Hours cannot be negative.")

    # 1. Base Case Condition: Check if hours <= 1 to halt recursion
    if hours <= 1:
        # 2. Base Definition: Return non-recursive baseline values (0 for h=0, 1 for h=1)
        return hours

    # 3. Recursive Case Condition: hours > 1
    # 4. Recursive Definition: P(h) = P(h - 1) + P(h - 2)
    return bacterial_population(hours - 1) + bacterial_population(hours - 2)


if __name__ == '__main__':
    print("=" * 45)
    print(f"{'Hour (h)':<10} {'Population':<15}")
    print("=" * 45)

    notes = {
        0: "(Baseline)",
        1: "(Initial mature cell)",
    }

    # Test loop for Hours 0 to 10
    for h in range(11           ):
        pop = bacterial_population(h)
        note = notes.get(h, "")
        print(f"{h:<10} {pop:<15} {note:<20}")

    print("=" * 45)
