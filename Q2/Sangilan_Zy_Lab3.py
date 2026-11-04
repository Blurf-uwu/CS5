# import math for floor and sqrt functions
import math

def calculate_cost(tolerance):
    """calculates cost based on tolerance"""
    return 1000 + tolerance ** 2


def find_optimal_tolerance(max_cost):
    """Finds the maximum integer tolerance (1 to 100) whose cost remains below max_cost
    using Binary Search. Returns -1 if no tolerance setting is acceptable

    could be done using:
    if max_cost > 1001:
        return floor(sqrt(max_cost - 1000))
    else:
        return -1
    """
    low = 1
    high = 100
    optimal_tolerance = -1

    while low <= high:
        mid = (low + high) // 2
        cost = calculate_cost(mid)

        if cost < max_cost:
            # mid is acceptable; track it and search for a higher acceptable tolerance
            optimal_tolerance = mid
            low = mid + 1
        else:
            # Cost is equal to or exceeds max_cost; reduce tolerance
            high = mid - 1

    return optimal_tolerance
"""
def opt2(cost):
    if cost > 1001:
        return math.floor(math.sqrt(cost - 1000))
    else:
        return -1
"""
def main():
    # header
    print("=" * 40)
    print(f"OPTIMAL TOLERANCE FINDER")
    print("=" * 40)

    #prompt
    to_find = int(input("Find: "))
    print(find_optimal_tolerance(to_find))
    # print(opt2(to_find))


if __name__ == "__main__":
    main()