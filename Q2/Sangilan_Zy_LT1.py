"""
================================================================================
                        SORTING ALGORITHM VISUALIZER
================================================================================

README & NOTES
--------------

1. PROGRAM OVERVIEW:
--------------------
This is an interactive terminal program that visualizes 5 canonical sorting
algorithms: Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, and Quick
Sort. 

This program uses ASCII star characters ('*') stacked vertically like a histogram, 
where the height of the stars directly represents each number in a list.

At the bottom of each column of stars, the exact integer value is printed
along with its array index. As the sort runs, elements are color-coded in the
terminal:
  - YELLOW:  Elements currently being COMPARED
  - RED:     Elements being SWAPPED or SHIFTED
  - MAGENTA: The PIVOT (Quick Sort) or KEY (Insertion Sort) or MIN (Selection)
  - GREEN:   Elements that are already locked into their final SORTED spot
  - CYAN:    Unsorted elements

2. HOW TO RUN:
--------------
Prerequisites:
  - Python 3.8 or above installed.
  - Run inside any terminal (PowerShell, Command Prompt, Bash) or any IDE (VSCode, PyCharm, etc.).

Flow:
  1. Prompts for the number of RANDOMIZED elements to sort (up to 10 elements).
  2. Generates random numbers and prints the initial list.
  3. Prompts for the sorting algorithm (1 to 5).
  4. Animates each comparison and swap step with a 0.5s delay.
  5. Shows a final summary and asks if you want to sort again (y/n).
     If you say 'n', the program stops.

3. HOW TO ADJUST BASIC PARAMETERS:
----------------------------------
Near the top of the code, you can tweak these variables to your liking:
  - DELAY: Set to 0.5 by default (seconds to pause per step so you can watch).
           Change to 0.1 for faster speed or 1.0 for super slow motion.
  - MAX_ELEMENTS: Maximum number of elements allowed (default is 10).
                  The random number range automatically scales with MAX_ELEMENTS
                  (max(15, MAX_ELEMENTS + 5)) so it never crashes if you increase it!
  - STAR_CHAR: Character used for the bars (default is "*", but you could use "#").

4. OUTLINE OF DATA STRUCTURES:
------------------------------
- Python List ('arr = [...]'):
  A mutable 1D dynamic array of integers. This holds the randomized numbers to
  be sorted in place.
- Helper Lists ('comparing = []', 'swapping = []', 'sorted_indices = []'):
  Simple lists of integer indices passed directly to draw_bars() to tell the
  visualizer which columns need to be highlighted in yellow, red, or green.
- Integer Counters:
  'step_count', 'comparisons_count', and 'swaps_count' track performance.

================================================================================
"""

# ==============================================================================
# IMPORTS & CITATIONS / DISCLAIMERS
# ==============================================================================
# DISCLAIMER:
# I didn't write all the terminal handling or color stuff completely from scratch.
# Here are the references and Stack Overflow posts I used and adapted:
#
# 1. os module: Used for clearing screen with 'cls' or 'clear'
#    https://stackoverflow.com/questions/2084508/clear-terminal-in-python
#
# 2. sys module: Used for stdout flushing and reconfiguring UTF-8 output
#    https://stackoverflow.com/questions/3777301/how-to-call-a-function-repeatedly-without-clearing-screen
#
# 3. time module: Used for time.sleep(0.5) to add the 0.5s delay between sort steps
#    https://stackoverflow.com/questions/510348/how-can-i-make-a-time-delay-in-python
#
# 4. random module: Used random.sample to get unique random integers
#    https://stackoverflow.com/questions/22842289/generate-n-unique-random-numbers-within-a-range
#
# 5. ANSI escape codes for colored text (Colors class):
#    https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
#
# 6. Windows virtual terminal VT100 fix (so ANSI colors work in cmd/powershell):
#    https://stackoverflow.com/questions/36760127/how-to-use-ansi-escape-codes-in-windows-command-prompt
#
# 7. Sorting algorithms canonical logic:
#    Adapted from GeeksforGeeks articles:
#    - Bubble Sort:    https://www.geeksforgeeks.org/bubble-sort/
#    - Selection Sort: https://www.geeksforgeeks.org/selection-sort/
#    - Insertion Sort: https://www.geeksforgeeks.org/insertion-sort/
#    - Merge Sort:     https://www.geeksforgeeks.org/merge-sort/
#    - Quick Sort:     https://www.geeksforgeeks.org/quick-sort/

import os
import sys
import time
import random


# ==============================================================================
# PARAMETERS & SETTINGS (FOR EASIER MODIFICATIONS)
# ==============================================================================
DELAY = 0.5             # x second pause between each step to show the process
MAX_ELEMENTS = 10       # up to n elements for the list
STAR_CHAR = "*"         # ASCII character used to draw the vertical bars


# ==============================================================================
# GLOBAL TRACKING VARIABLES
# ==============================================================================
step_count = 0
comparisons_count = 0
swaps_count = 0
current_algo_name = ""


# ==============================================================================
# COLOR CLASS
# ==============================================================================
# from Stack Overflow:
# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    # Colors for different roles
    RED = "\033[91m"          # Swapping or shifting elements
    GREEN = "\033[92m"        # Sorted / placed elements
    YELLOW = "\033[93m"       # Elements currently being compared
    BLUE = "\033[94m"         # Borders and titles
    MAGENTA = "\033[95m"      # Pivot in Quick Sort or key in Insertion
    CYAN = "\033[96m"         # Default unsorted bars
    WHITE = "\033[97m"        # Values and text
    GRAY = "\033[90m"         # Subtle lines and brackets

    # Terminal cursor movement
    CLEAR_EOL = "\033[K"      # Erase from cursor to end of line


# ==============================================================================
# TERMINAL HELPERS
# ==============================================================================
def init_terminal():
    """
    Sets up terminal encoding and Windows ANSI escape support.
    Reference: https://stackoverflow.com/questions/36760127/how-to-use-ansi-escape-codes-in-windows-command-prompt
    """
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    if os.name == "nt":
        os.system("")


def clear_screen():
    """
    Clears the whole terminal screen.
    Reference: https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    """
    os.system("cls" if os.name == "nt" else "clear")


def cursor_home():
    """
    Moves cursor back to row 1, col 1 without clearing, which stops flickering!
    Reference: https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
    """
    sys.stdout.write("\033[H")
    sys.stdout.flush()


def hide_cursor():
    """
    Hides cursor while animating to prevent cursor flicker.
    Reference: https://stackoverflow.com/questions/2330245/how-to-hide-cursor-in-terminal-with-python
    """
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor():
    """
    Brings cursor back when finished or interrupted.
    Reference: https://stackoverflow.com/questions/2330245/how-to-hide-cursor-in-terminal-with-python
    """
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


# ==============================================================================
# VISUALIZER 
# ==============================================================================
def draw_bars(arr, comparing=[], swapping=[], pivot=-1, sorted_indices=[], action=""):
    """
    Draws the array as vertical ASCII star (*) bars with values at the bottom.
    
    Parameters:
      arr            - the current list of numbers
      comparing      - list of indices being compared (colored YELLOW)
      swapping       - list of indices being swapped or shifted (colored RED)
      pivot          - index of pivot/key/min (colored MAGENTA)
      sorted_indices - list of indices confirmed to be in sorted order (colored GREEN)
      action         - explanation text of what just happened
    """
    global step_count, comparisons_count, swaps_count

    step_count += 1
    if comparing:
        comparisons_count += 1
    if swapping:
        swaps_count += 1

    n = len(arr)
    max_val = max(arr) if arr else 1
    # For small numbers (<= 14), 1 star = 1 unit.
    # If someone tests large numbers, cap chart height at 14 rows so it fits on screen.
    chart_h = min(max_val, 14)
    width = max(55, n * 5 + 10)

    lines = []

    # 1. Header
    lines.append(f"{Colors.BLUE}{'=' * width}{Colors.RESET}{Colors.CLEAR_EOL}")
    title_text = f"SORTING VISUALIZER: {current_algo_name.upper()}"
    lines.append(f"{Colors.BOLD}{Colors.WHITE}{title_text.center(width)}{Colors.RESET}{Colors.CLEAR_EOL}")
    lines.append(f"{Colors.BLUE}{'=' * width}{Colors.RESET}{Colors.CLEAR_EOL}")

    # 2. Stats
    lines.append(
        f" Step: {Colors.WHITE}{step_count:<3}{Colors.RESET} | "
        f"Comparisons: {Colors.YELLOW}{comparisons_count:<3}{Colors.RESET} | "
        f"Swaps/Writes: {Colors.RED}{swaps_count:<3}{Colors.RESET} | "
        f"Delay: {Colors.CYAN}{DELAY:.1f}s/step{Colors.RESET}"
        f"{Colors.CLEAR_EOL}"
    )
    lines.append(f"{Colors.GRAY}{'-' * width}{Colors.RESET}{Colors.CLEAR_EOL}")

    # 3. Draw vertical ASCII star bars
    # We go from row = chart_h down to 1
    for level in range(chart_h, 0, -1):
        row = "  "
        for idx in range(n):
            val = arr[idx]
            # Height in stars: exact val if max_val <= 14, else scaled
            bar_height = val if max_val <= 14 else max(1, round((val / max_val) * 14))

            # Choose color based on what the element is doing
            if idx in swapping:
                col = Colors.RED
            elif idx in comparing:
                col = Colors.YELLOW
            elif idx == pivot:
                col = Colors.MAGENTA
            elif idx in sorted_indices:
                col = Colors.GREEN
            else:
                col = Colors.CYAN

            # If the value is high enough, print a star, otherwise print empty spaces
            if bar_height >= level:
                row = row + f"  {col}{STAR_CHAR}{Colors.RESET} "
            else:
                row = row + "    "
        lines.append(f"{row}{Colors.CLEAR_EOL}")

    # 4. Bottom horizontal line
    lines.append(f"{Colors.GRAY}  {'-' * (n * 4)}{Colors.RESET}{Colors.CLEAR_EOL}")

    # 5. Values row at the bottom of the bars
    val_row = "  "
    for idx in range(n):
        val = arr[idx]
        if idx in swapping:
            col = Colors.RED
        elif idx in comparing:
            col = Colors.YELLOW
        elif idx == pivot:
            col = Colors.MAGENTA
        elif idx in sorted_indices:
            col = Colors.GREEN
        else:
            col = Colors.WHITE
        val_row = val_row + f"{col}{val:>3}{Colors.RESET} "
    lines.append(f"{val_row}{Colors.CLEAR_EOL}")

    # 6. Index row underneath values
    idx_row = "  "
    for i in range(n):
        idx_row = idx_row + f"{Colors.GRAY}[{i}] {Colors.RESET}"
    lines.append(f"{idx_row}{Colors.CLEAR_EOL}")

    # 7. Legend
    lines.append(f"{Colors.GRAY}{'-' * width}{Colors.RESET}{Colors.CLEAR_EOL}")
    legend = (
        f" Legend: {Colors.YELLOW}* Compare{Colors.RESET}  "
        f"{Colors.RED}* Swap/Shift{Colors.RESET}  "
        f"{Colors.MAGENTA}* Pivot/Key{Colors.RESET}  "
        f"{Colors.GREEN}* Sorted{Colors.RESET}"
    )
    lines.append(f"{legend}{Colors.CLEAR_EOL}")

    # 8. Array as a text list
    arr_text = ", ".join(str(x) for x in arr)
    lines.append(f" Array:  [ {arr_text} ]{Colors.CLEAR_EOL}")

    # 9. Action explanation
    lines.append(f" Action: {Colors.WHITE}{action}{Colors.RESET}{Colors.CLEAR_EOL}")
    lines.append(f"{Colors.BLUE}{'=' * width}{Colors.RESET}{Colors.CLEAR_EOL}")

    # Move cursor to top-left and print all lines at once to prevent screen flickering
    cursor_home()
    sys.stdout.write("\n".join(lines) + "\n")
    sys.stdout.flush()

    # Sleep 0.5 seconds so user can watch the sorting step
    time.sleep(DELAY)


# ==============================================================================
# SORTING ALGORITHMS
# ==============================================================================

# 1. BUBBLE SORT
def bubble_sort(arr):
    """
    Bubble Sort:
    Repeatedly loops through the list, compares adjacent items, and swaps
    them if the left item is greater than the right item.
    Includes early-exit check if no swaps happen.
    
    Reference: https://www.geeksforgeeks.org/bubble-sort/
    """
    n = len(arr)
    sorted_indices = []

    for i in range(n):
        swapped = False
        # Inner loop to compare adjacent elements
        for j in range(0, n - i - 1):
            # Show comparison
            draw_bars(arr, comparing=[j, j + 1], sorted_indices=sorted_indices,
                      action=f"Comparing arr[{j}] ({arr[j]}) and arr[{j+1}] ({arr[j+1]})")

            if arr[j] > arr[j + 1]:
                # Swap elements
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                # Show swap
                draw_bars(arr, swapping=[j, j + 1], sorted_indices=sorted_indices,
                          action=f"Swapped: arr[{j}] <-> arr[{j+1}] ({arr[j]} < {arr[j+1]})")

        # After each pass, the biggest remaining element reaches its final place
        sorted_indices.append(n - i - 1)
        draw_bars(arr, sorted_indices=sorted_indices,
                  action=f"Pass {i+1} done: {arr[n - i - 1]} is locked into place.")

        # Early exit optimization: if nothing was swapped in a pass, it's already sorted!
        if not swapped:
            draw_bars(arr, sorted_indices=list(range(n)),
                      action="Early exit! No swaps were needed, array is sorted.")
            break


# 2. SELECTION SORT
def selection_sort(arr):
    """
    Selection Sort:
    Divides list into sorted part and unsorted part. Scans unsorted part to
    find the smallest value, then swaps it with the first unsorted item.
    
    Reference: https://www.geeksforgeeks.org/selection-sort/
    """
    n = len(arr)
    sorted_indices = []

    for i in range(n):
        # Start by assuming the first unsorted item is the minimum
        min_idx = i
        draw_bars(arr, pivot=min_idx, sorted_indices=sorted_indices,
                  action=f"Pass {i+1}: Started looking for minimum, assuming it's arr[{i}] ({arr[i]})")

        # Scan the rest of the array to find if there's any smaller item
        for j in range(i + 1, n):
            draw_bars(arr, comparing=[j], pivot=min_idx, sorted_indices=sorted_indices,
                      action=f"Comparing arr[{j}] ({arr[j]}) with current min arr[{min_idx}] ({arr[min_idx]})")

            if arr[j] < arr[min_idx]:
                min_idx = j
                draw_bars(arr, pivot=min_idx, sorted_indices=sorted_indices,
                          action=f"New minimum found! arr[{min_idx}] = {arr[min_idx]}")

        # Swap the found minimum into index i
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            sorted_indices.append(i)
            draw_bars(arr, swapping=[i, min_idx], sorted_indices=sorted_indices,
                      action=f"Swapped minimum {arr[i]} into sorted position at index [{i}]")
        else:
            sorted_indices.append(i)
            draw_bars(arr, sorted_indices=sorted_indices,
                      action=f"Index [{i}] was already the minimum ({arr[i]}), no swap needed.")


# 3. INSERTION SORT
def insertion_sort(arr):
    """
    Insertion Sort:
    Takes items one by one (the 'key') and shifts any larger items in the
    sorted prefix one slot to the right, then drops the key into place.
    
    Reference: https://www.geeksforgeeks.org/insertion-sort/
    """
    n = len(arr)

    for i in range(1, n):
        key = arr[i]
        j = i - 1
        sorted_indices = list(range(i))

        draw_bars(arr, pivot=i, sorted_indices=sorted_indices,
                  action=f"Picked key = {key} at index [{i}] to insert into sorted prefix")

        # Shift elements of arr[0..i-1] that are greater than key to one position ahead
        while j >= 0:
            draw_bars(arr, comparing=[j], pivot=j + 1, sorted_indices=[k for k in range(i) if k != j],
                      action=f"Comparing key ({key}) with arr[{j}] ({arr[j]})")

            if arr[j] > key:
                arr[j + 1] = arr[j]
                draw_bars(arr, swapping=[j + 1], comparing=[j], sorted_indices=[k for k in range(i) if k != j and k != j + 1],
                          action=f"arr[{j}] ({arr[j]}) > key ({key}): Shifted {arr[j]} right to index [{j+1}]")
                j = j - 1
            else:
                break

        # Put key into its correct position
        arr[j + 1] = key
        draw_bars(arr, swapping=[j + 1], sorted_indices=list(range(i + 1)),
                  action=f"Inserted key ({key}) into position [{j+1}]")


# 4. MERGE SORT
def merge_sort(arr):
    """
    Merge Sort:
    Recursive divide-and-conquer algorithm.
    Splits list into two halves, sorts each half, and merges them back in order.
    
    Reference: https://www.geeksforgeeks.org/merge-sort/
    """
    def _merge_sort_helper(low, high):
        if low >= high:
            return

        mid = (low + high) // 2
        draw_bars(arr, comparing=list(range(low, high + 1)),
                  action=f"Divide: Splitting sub-list [{low}..{high}] at midpoint {mid}")

        # Recursively sort left and right halves
        _merge_sort_helper(low, mid)
        _merge_sort_helper(mid + 1, high)

        # Merge step using temporary lists
        left_copy = arr[low:mid + 1]
        right_copy = arr[mid + 1:high + 1]

        p1 = 0
        p2 = 0
        k = low

        while p1 < len(left_copy) and p2 < len(right_copy):
            orig_left = low + p1
            orig_right = mid + 1 + p2
            draw_bars(arr, comparing=[orig_left, orig_right], pivot=k,
                      action=f"Comparing left element {left_copy[p1]} and right element {right_copy[p2]}")

            if left_copy[p1] <= right_copy[p2]:
                arr[k] = left_copy[p1]
                p1 += 1
            else:
                arr[k] = right_copy[p2]
                p2 += 1

            draw_bars(arr, swapping=[k],
                      action=f"Merged {arr[k]} into index [{k}]")
            k += 1

        # Copy any leftover elements from left side
        while p1 < len(left_copy):
            arr[k] = left_copy[p1]
            draw_bars(arr, swapping=[k],
                      action=f"Copied leftover left item {arr[k]} to index [{k}]")
            p1 += 1
            k += 1

        # Copy any leftover elements from right side
        while p2 < len(right_copy):
            arr[k] = right_copy[p2]
            draw_bars(arr, swapping=[k],
                      action=f"Copied leftover right item {arr[k]} to index [{k}]")
            p2 += 1
            k += 1

    _merge_sort_helper(0, len(arr) - 1)


# 5. QUICK SORT
def quick_sort(arr):
    """
    Quick Sort (using canonical Lomuto partitioning):
    Chooses the last element as the pivot, moves all elements smaller than
    or equal to pivot to the left side, places the pivot in the middle, and
    recursively sorts the left and right halves.
    
    Reference: https://www.geeksforgeeks.org/quick-sort/
    """
    def _quick_sort_helper(low, high):
        if low < high:
            pivot = arr[high]
            i = low - 1
            draw_bars(arr, pivot=high,
                      action=f"Partitioning range [{low}..{high}] with pivot arr[{high}] = {pivot}")

            for j in range(low, high):
                draw_bars(arr, comparing=[j], pivot=high,
                          action=f"Comparing arr[{j}] ({arr[j]}) with pivot ({pivot})")

                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    draw_bars(arr, swapping=[i, j], pivot=high,
                              action=f"arr[{j}] <= pivot ({pivot}): Swapped arr[{i}] <-> arr[{j}]")

            # Place pivot into its correct locked position
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            pivot_idx = i + 1
            draw_bars(arr, sorted_indices=[pivot_idx],
                      action=f"Pivot {pivot} placed in its final position at index [{pivot_idx}]")

            # Recursively sort left and right partitions
            _quick_sort_helper(low, pivot_idx - 1)
            _quick_sort_helper(pivot_idx + 1, high)

    _quick_sort_helper(0, len(arr) - 1)

# ==============================================================================
# STATS
# ==============================================================================
def run_sort_demo(arr, algo_choice):
    """
    Prepares stats, runs the chosen sort, and shows the completion summary.
    """
    global current_algo_name, step_count, comparisons_count, swaps_count

    # Reset metrics counters
    step_count = 0
    comparisons_count = 0
    swaps_count = 0

    algo_names = {
        1: "Bubble Sort",
        2: "Selection Sort",
        3: "Insertion Sort",
        4: "Merge Sort",
        5: "Quick Sort"
    }
    current_algo_name = algo_names[algo_choice]

    clear_screen()
    hide_cursor()

    # Draw the initial state before sorting starts
    draw_bars(arr, action=f"Initial array before starting {current_algo_name}")

    try:
        # Run selected sorting algorithm
        if algo_choice == 1:
            bubble_sort(arr)
        elif algo_choice == 2:
            selection_sort(arr)
        elif algo_choice == 3:
            insertion_sort(arr)
        elif algo_choice == 4:
            merge_sort(arr)
        elif algo_choice == 5:
            quick_sort(arr)

        # Final all-green celebration frame
        all_sorted = list(range(len(arr)))
        draw_bars(arr, sorted_indices=all_sorted,
                  action=f"SORT COMPLETED SUCCESSFULLY! Array is 100% sorted in ascending order.")

    except KeyboardInterrupt:
        # If user presses Ctrl+C, don't crash
        cursor_home()
        print(f"\n{Colors.RED}Sorting stopped by user (Ctrl+C).{Colors.RESET}")
    finally:
        show_cursor()

    # Post-sort summary card
    print("\n" + "=" * 55)
    print(f" {current_algo_name.upper()} PROCESS COMPLETE!")
    print(f" Final sorted array: {arr}")
    print(f" Total steps:        {step_count}")
    print(f" Total comparisons:  {comparisons_count}")
    print(f" Total swaps/writes: {swaps_count}")
    print("=" * 55 + "\n")

# ==============================================================================
# USER INPUT
# ==============================================================================
def get_number_of_elements():
    """
    Prompt user for number of randomized elements to use in demo (up to 10 elements).
    Includes a try-except validation loop so it doesn't crash on invalid input.
    """
    while True:
        try:
            ans = input(f"Enter number of RANDOMIZED elements to sort (1 to {MAX_ELEMENTS}): ").strip()
            num = int(ans)
            if 1 <= num <= MAX_ELEMENTS:
                return num
            else:
                print(f"  [!] Please pick a number between 1 and {MAX_ELEMENTS}!\n")
        except ValueError:
            print("  [!] Invalid input! Please enter a whole number (integer).\n")

def get_sort_choice():
    """
    Prompt user for the type of sort.
    """
    print("\nSelect a sorting algorithm to visualize:")
    print("  [1] Bubble Sort    - compares adjacent items & early-exit swaps")
    print("  [2] Selection Sort - finds minimum element & swaps to front")
    print("  [3] Insertion Sort - shifts bigger items to insert key into sorted part")
    print("  [4] Merge Sort     - divides list in halves and merges back")
    print("  [5] Quick Sort     - partitions list around a pivot element")

    while True:
        choice = input("\nEnter algorithm choice (1-5): ").strip()
        if choice in ("1", "2", "3", "4", "5"):
            return int(choice)
        print("  [!] Invalid choice! Please enter a number from 1 to 5.")

def ask_go_again():
    """
    Prompt user if they want to go again. Stop program if user says no.
    """
    while True:
        ans = input("Would you like to sort another array? (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        elif ans in ("n", "no"):
            return False
        print("  [!] Please type 'y' for yes or 'n' for no.")

# ==============================================================================
# MAIN 
# ==============================================================================
def main():
    """
    Program flow:
      1. prompt user for number of RANDOMIZED elements (up to 10 elements)
      2. prompt user for type of sort
      3. show how sort is done with x sec delay per sort to show the process
      4. once done, prompt user if they want to go again. stop program if user says no.
    """
    init_terminal()

    while True:
        clear_screen()
        print("=" * 55)
        print("             SORTING ALGORITHM VISUALIZER")
        print("=" * 55 + "\n")

        # 1. Prompt user for number of randomized elements (up to n)
        n = get_number_of_elements()

        # The range scales with MAX_ELEMENTS and n so:
        # There are always enough unique numbers for random.sample (no ValueError)
        max_pool = max(15, max(n, MAX_ELEMENTS) + 5)
        arr = random.sample(range(1, max_pool), n)
        print(f"\n  Generated Random Array: {arr}")

        # 2. Prompt user for type of sort
        algo_choice = get_sort_choice()

        # 3. Show how sort is done with 0.5s delay
        run_sort_demo(arr, algo_choice)

        # 4. Once done, prompt user if they want to go again; stop if user says no
        if not ask_go_again():
            print("\nThank you for using the Sorting Visualizer! Goodbye.\n")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        show_cursor()
        print("\n\nProgram stopped by user. Goodbye!\n")
        sys.exit(0)
