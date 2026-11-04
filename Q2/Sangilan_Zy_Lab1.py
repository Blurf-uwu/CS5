def bubble_sort(arr):
    """Sorts a list in ascending order using the Bubble Sort algorithm"""
    n = len(arr)
    for i in range(n):
        swapped = False
        # Inner loop to compare adjacent elements
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                # Swap elements if they are in the wrong order
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # If no elements were swapped, list is already sorted
        if not swapped:
            break
    return arr


def binary_search(arr, target):
    """Searches for target in a sorted list using Binary Search.
    Returns index of target if found, else -1
    """
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


def main():
    # Input 10 integerrs
    numbers = [int(x) for x in input("Enter 10 Numbers: ").split()]
    target = int(input("Enter number to search for: "))
    
    # Sort and print sorted list
    sorted_numbers = bubble_sort(numbers)
    print("Sorted List:", *sorted_numbers)

    # Search using Binary Search
    result = binary_search(sorted_numbers, target)
    if result != -1:
        print(f"{target} is in the collection")
    else:
        print(f"{target} is not in the collection")

# Run program
main()