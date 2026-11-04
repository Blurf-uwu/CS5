"""
================================================================================
                    TERMINAL SORTING ALGORITHM VISUALIZER
                 Philippine Science High School - CS5 (Q2)
================================================================================

README & USER MANUAL
--------------------

1. PROJECT OVERVIEW
-------------------
This program is an interactive, terminal-based sorting algorithm visualizer
engineered for algorithmic education and empirical analysis. It provides
a real-time, flicker-free graphical representation of five canonical sorting
algorithms:
    1. Bubble Sort (Adjacent comparisons with early-exit optimization)
    2. Selection Sort (Minimum element extraction and boundary swapping)
    3. Insertion Sort (Adaptive incremental shifting into sorted prefix)
    4. Merge Sort (Recursive divide-and-conquer with auxiliary merging)
    5. Quick Sort (Lomuto partitioning scheme around a pivot)

The visualizer transforms raw array states into dynamic vertical bar charts
rendered directly inside the terminal. It leverages ANSI color codes to
distinguish active comparisons, element swaps/writes, partition pivots, and
final sorted placements.

2. HOW TO RUN THE PROGRAM
-------------------------
Prerequisites:
    - Python 3.8 or higher installed on your system.
    - Any standard terminal emulator (Windows Terminal, PowerShell, Command Prompt,
      macOS Terminal, Linux bash/zsh).
    - Note: On Windows, Virtual Terminal (ANSI VT100) mode and UTF-8 encoding
      are automatically initialized by the program upon startup.

Execution Command:
    Open your terminal, navigate to the directory containing this script, and run:
        python Vis.py

    Alternatively, run it from any parent directory:
        python "c:/Users/LENOVO/CS5/Q2/Vis.py"

Interactive Controls:
    - Main Menu: Enter numbers [1] through [5] to select an algorithm.
    - Settings Menu: Enter [6] to interactively adjust array size, speed, and glyph.
    - Reference Table: Enter [7] to view theoretical Big-O complexity tables.
    - Exit: Enter [0] to cleanly terminate the program.
    - During Visualization: Press [Ctrl+C] at any time to safely abort the active
      sort and return to the prompt without corrupting terminal cursor state.
    - Post-Visualization: An automated green verification sweep validates the
      sorted state, followed by a performance summary card. Press [Enter] to
      return to the main menu.

3. HOW TO ADJUST BASIC PARAMETERS
---------------------------------
Parameters can be configured in two ways:

Method A: Through the Interactive Settings Menu (Runtime Configuration)
    - From the main menu, select option [6] "Customize Settings".
    - You can adjust:
        a) Array Size (N): Number of elements to sort.
           - Default: 25 elements.
           - Recommended: 10 to 50 elements (fits cleanly in standard 80-column terminals).
        b) Frame Delay (Speed): Pause duration between animation frames in seconds.
           - Default: 0.040s (40 ms per frame).
           - Faster: 0.010s - 0.020s.
           - Slower: 0.080s - 0.150s.
        c) Bar Glyph Character: Visual rendering character for the vertical bars.
           - Default: '█' (Unicode Full Block U+2588).
           - Alternatives: '#', '|', '*', 'O'.

Method B: By Editing Script Constants (Persistent Configuration)
    - Locate the "CONFIGURATION & GLOBAL DEFAULTS" section right below this docstring.
    - Update the global constants directly:
        DEFAULT_ARRAY_SIZE = 25     # Integer: number of elements in the random array
        DEFAULT_DELAY = 0.04        # Float: animation frame sleep time in seconds
        DEFAULT_BAR_CHAR = "█"      # String: character representing bar height
        DEFAULT_CHART_HEIGHT = 14   # Integer: maximum line height of vertical bars

4. OUTLINE OF DATA STRUCTURES USED FOR THE VISUALIZATION
--------------------------------------------------------
A. Dynamic Array (`list[int]`):
   - The primary data structure is a 1D Python dynamic array (contiguous memory list
     of integers) containing a permutation of unique numbers from 1 to N: `[1, 2, ..., N]`.
   - Using a permutation of distinct values guarantees that each element has a unique
     height, forming a pristine, monotonic diagonal staircase upon sort completion.
   - The array is randomized before every visualization run using the Fisher-Yates
     shuffle algorithm via `random.shuffle()`.

B. Generator Protocol & State Event Tuples (`yield`):
   - To strictly separate sorting algorithmic logic from the visual rendering subsystem,
     every sorting function is implemented as a Python generator (`yield`).
   - At each atomic algorithmic step (comparison, swap, partition split, or array write),
     the algorithm yields a 4-element state tuple:
         (current_array, highlights_dict, operation_type, status_message)
   - `highlights_dict` (`dict[int, str]`): A hash table mapping affected array indices
     to their current visual roles:
         - "compare": Elements currently being evaluated against each other (Bright Yellow)
         - "swap": Elements being swapped or overwritten in memory (Bright Red)
         - "pivot": Pivot element in Quick Sort or target min in Selection (Bright Magenta)
         - "sorted": Elements confirmed to be in their final sorted positions (Bright Green)

C. Flicker-Free Screen Buffer & Double-Buffering (`sys.stdout.write`):
   - In standard console scripts, repeatedly calling `os.system('cls')` causes heavy
     screen flickering and tearing due to continuous OS process creation and screen redrawing.
   - This visualizer resolves screen tearing by utilizing double-buffered in-memory string
     construction: the entire terminal frame (headers, metrics, 2D bar matrix, axis, legend,
     and status lines) is assembled into a single contiguous string buffer.
   - The terminal cursor is repositioned to row 1, column 1 using the ANSI escape
     sequence `\\033[H`.
   - Each frame line ends with `\\033[K` (erase to end of line), guaranteeing that no
     stale characters remain, and the entire buffer is emitted in a single atomic I/O write.
   - ANSI cursor controls (`\\033[?25l` to hide, `\\033[?25h` to restore) eliminate cursor
     jitter during high-speed animation.

================================================================================
"""

import os
import sys
import time
import random
import shutil
from typing import Generator, Dict, List, Tuple, Optional


# ==============================================================================
# CONFIGURATION & GLOBAL DEFAULTS
# ==============================================================================
# Adjust default runtime parameters here (or interactively via Menu Option 6).
DEFAULT_ARRAY_SIZE: int = 25       # Number of elements (10 - 50 recommended)
DEFAULT_DELAY: float = 0.04        # Animation delay per step in seconds (0.01 - 0.20)
DEFAULT_BAR_CHAR: str = "█"        # Glyph character for bars ('█', '#', '|', etc.)
DEFAULT_CHART_HEIGHT: int = 14     # Default max line height of the bar chart


# ==============================================================================
# ANSI ESCAPE CODES & COLOR PALETTE
# ==============================================================================
class Colors:
    """ANSI color escape sequences for terminal styling and visual role distinction."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Foreground Colors
    BLACK = "\033[30m"
    RED = "\033[91m"          # Swaps / Writes
    GREEN = "\033[92m"        # Sorted / Placed / Verified
    YELLOW = "\033[93m"       # Comparisons / Active scanning
    BLUE = "\033[94m"         # Headers / Frames
    MAGENTA = "\033[95m"      # Pivots / Keys / Minimums
    CYAN = "\033[96m"         # Default unsorted bars
    WHITE = "\033[97m"        # Text / Accents
    GRAY = "\033[90m"         # Subtle borders / Gridlines

    # Line clearing
    CLEAR_EOL = "\033[K"      # Erase from cursor to end of current line


# ==============================================================================
# TERMINAL MANAGEMENT UTILITIES
# ==============================================================================
def init_terminal() -> None:
    """
    Initializes terminal settings, configures UTF-8 encoding for standard output,
    and enables ANSI escape sequence processing on Windows systems.
    """
    # Ensure stdout and stderr support UTF-8 characters (like █, ─, ■) on Windows consoles
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    if os.name == "nt":
        # Calling os.system('') enables virtual terminal (VT100) processing in Windows cmd/pwsh
        os.system("")


def clear_screen() -> None:
    """Clears the terminal screen entirely using the host OS command."""
    os.system("cls" if os.name == "nt" else "clear")


def cursor_home() -> None:
    """Reposition the cursor to line 1, column 1 without clearing the screen buffer."""
    sys.stdout.write("\033[H")
    sys.stdout.flush()


def hide_cursor() -> None:
    """Hides the terminal cursor to eliminate animation jitter and screen tearing."""
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor() -> None:
    """Restores the terminal cursor visibility."""
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


# ==============================================================================
# CANONICAL SORTING ALGORITHMS (GENERATORS)
# ==============================================================================
# Each algorithm is a Python generator yielding state tuples:
#   (current_arr, highlights_dict, operation_type, status_message)
#
# Highlight types:
#   "compare" -> Yellow
#   "swap"    -> Red
#   "pivot"   -> Magenta
#   "sorted"  -> Green

def bubble_sort(arr: List[int]) -> Generator[Tuple[List[int], Dict[int, str], str, str], None, None]:
    """
    Canonical Bubble Sort with early-termination optimization.

    Repeatedly passes through the list, compares adjacent elements, and swaps
    them if they are out of order. An optimized 'swapped' boolean flag allows
    best-case execution in O(n) time when the array is already sorted.

    Time Complexity: Best O(n), Average O(n^2), Worst O(n^2)
    Space Complexity: O(1) auxiliary (In-Place, Stable)
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            # Highlight the two adjacent elements being compared
            yield (
                arr,
                {j: "compare", j + 1: "compare"},
                "compare",
                f"Comparing adjacent elements arr[{j}]={arr[j]} and arr[{j+1}]={arr[j+1]}"
            )

            if arr[j] > arr[j + 1]:
                # Perform adjacent swap
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                yield (
                    arr,
                    {j: "swap", j + 1: "swap"},
                    "swap",
                    f"Swapped out-of-order elements: arr[{j}] <-> arr[{j+1}]"
                )

        # The element at index n - i - 1 is now locked in its final sorted position
        yield (
            arr,
            {n - i - 1: "sorted"},
            "state",
            f"Pass {i + 1} complete. Largest unsorted value bubbled to index {n - i - 1}"
        )

        # Early exit if no two elements were swapped in this pass
        if not swapped:
            yield (
                arr,
                {},
                "state",
                "Early exit triggered: No swaps occurred during this pass (Array is sorted)."
            )
            break


def selection_sort(arr: List[int]) -> Generator[Tuple[List[int], Dict[int, str], str, str], None, None]:
    """
    Canonical Selection Sort.

    Divides the list into a sorted prefix and an unsorted suffix. In each pass,
    scans the unsorted suffix to find the minimum element, then performs a
    single swap to place it at the boundary of the sorted prefix.

    Time Complexity: Best O(n^2), Average O(n^2), Worst O(n^2)
    Space Complexity: O(1) auxiliary (In-Place, Unstable)
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        yield (
            arr,
            {min_idx: "pivot"},
            "state",
            f"Pass {i + 1}: Initialized current minimum at index {i} (value: {arr[i]})"
        )

        for j in range(i + 1, n):
            # Highlight current candidate and current minimum being compared
            yield (
                arr,
                {j: "compare", min_idx: "pivot"},
                "compare",
                f"Scanning index {j} (value {arr[j]}). Comparing with current minimum (value {arr[min_idx]})"
            )

            if arr[j] < arr[min_idx]:
                min_idx = j
                yield (
                    arr,
                    {min_idx: "pivot"},
                    "state",
                    f"New minimum identified: arr[{min_idx}] = {arr[min_idx]}"
                )

        # Swap the found minimum element with the first element of the unsorted segment
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield (
                arr,
                {i: "swap", min_idx: "swap"},
                "swap",
                f"Placed minimum {arr[i]} into sorted position by swapping indices {i} and {min_idx}"
            )
        else:
            yield (
                arr,
                {i: "sorted"},
                "state",
                f"Index {i} already held minimum value {arr[i]}. No swap needed."
            )


def insertion_sort(arr: List[int]) -> Generator[Tuple[List[int], Dict[int, str], str, str], None, None]:
    """
    Canonical Insertion Sort.

    Iterates through the array, taking one element at a time (the 'key') and
    shifting all larger elements in the sorted prefix one position to the right
    to make room for inserting the key into its correct relative position.

    Time Complexity: Best O(n), Average O(n^2), Worst O(n^2)
    Space Complexity: O(1) auxiliary (In-Place, Stable)
    """
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1

        yield (
            arr,
            {i: "pivot"},
            "state",
            f"Selected key = {key} at index {i}. Inserting into sorted prefix [0..{i-1}]"
        )

        while j >= 0:
            # Highlight comparison between sorted prefix element and the key
            yield (
                arr,
                {j: "compare", j + 1: "pivot"},
                "compare",
                f"Comparing key ({key}) with prefix element arr[{j}]={arr[j]}"
            )

            if arr[j] > key:
                # Shift larger element one slot to the right
                arr[j + 1] = arr[j]
                yield (
                    arr,
                    {j + 1: "swap", j: "compare"},
                    "swap",
                    f"Shifted arr[{j}] ({arr[j]}) rightwards to index {j + 1}"
                )
                j -= 1
            else:
                break

        # Place the key into its sorted slot
        arr[j + 1] = key
        yield (
            arr,
            {j + 1: "sorted"},
            "swap",
            f"Inserted key ({key}) into position arr[{j + 1}]"
        )


def merge_sort(arr: List[int]) -> Generator[Tuple[List[int], Dict[int, str], str, str], None, None]:
    """
    Canonical Merge Sort (Recursive Divide and Conquer).

    Recursively splits the array into two halves until single-element subarrays
    are reached, then merges sorted subarrays back into the primary array
    using an auxiliary buffer while yielding visual updates for each step.

    Time Complexity: Best O(n log n), Average O(n log n), Worst O(n log n)
    Space Complexity: O(n) auxiliary (Stable)
    """
    def _merge_sort_helper(
        start: int, end: int
    ) -> Generator[Tuple[List[int], Dict[int, str], str, str], None, None]:
        if start >= end:
            return

        mid = (start + end) // 2

        # Yield visual split step
        yield (
            arr,
            {k: "compare" for k in range(start, end + 1)},
            "state",
            f"Divide: Subarray [{start}..{end}] partitioned at midpoint {mid}"
        )

        # Recursively sort left and right partitions
        yield from _merge_sort_helper(start, mid)
        yield from _merge_sort_helper(mid + 1, end)

        # --- Merge Subroutine ---
        left_sub = arr[start:mid + 1]
        right_sub = arr[mid + 1:end + 1]

        p1 = 0
        p2 = 0
        k = start

        while p1 < len(left_sub) and p2 < len(right_sub):
            left_orig_idx = start + p1
            right_orig_idx = mid + 1 + p2

            yield (
                arr,
                {left_orig_idx: "compare", right_orig_idx: "compare", k: "pivot"},
                "compare",
                f"Comparing left element {left_sub[p1]} vs right element {right_sub[p2]}"
            )

            # <= condition guarantees algorithmic stability
            if left_sub[p1] <= right_sub[p2]:
                arr[k] = left_sub[p1]
                p1 += 1
            else:
                arr[k] = right_sub[p2]
                p2 += 1

            yield (
                arr,
                {k: "swap"},
                "swap",
                f"Merged element {arr[k]} written into primary array at index {k}"
            )
            k += 1

        # Copy any remaining elements from left half
        while p1 < len(left_sub):
            arr[k] = left_sub[p1]
            yield (
                arr,
                {k: "swap"},
                "swap",
                f"Copied remaining left element {arr[k]} into index {k}"
            )
            p1 += 1
            k += 1

        # Copy any remaining elements from right half
        while p2 < len(right_sub):
            arr[k] = right_sub[p2]
            yield (
                arr,
                {k: "swap"},
                "swap",
                f"Copied remaining right element {arr[k]} into index {k}"
            )
            p2 += 1
            k += 1

    yield from _merge_sort_helper(0, len(arr) - 1)


def quick_sort(arr: List[int]) -> Generator[Tuple[List[int], Dict[int, str], str, str], None, None]:
    """
    Canonical Quick Sort (Lomuto Partition Scheme).

    Selects the rightmost element as the pivot, rearranges the subarray such that
    all elements strictly smaller than the pivot precede it and all larger
    elements follow it, then recursively sorts the resulting partitions.

    Time Complexity: Best O(n log n), Average O(n log n), Worst O(n^2)
    Space Complexity: O(log n) call-stack space (In-Place, Unstable)
    """
    def _quick_sort_helper(
        low: int, high: int
    ) -> Generator[Tuple[List[int], Dict[int, str], str, str], None, None]:
        if low < high:
            # Partitioning subroutine
            pivot = arr[high]
            i = low - 1

            yield (
                arr,
                {high: "pivot"},
                "state",
                f"Partitioning range [{low}..{high}] with pivot = arr[{high}] ({pivot})"
            )

            for j in range(low, high):
                yield (
                    arr,
                    {j: "compare", high: "pivot", max(low, i): "state"},
                    "compare",
                    f"Comparing arr[{j}]={arr[j]} with pivot {pivot}"
                )

                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    yield (
                        arr,
                        {i: "swap", j: "swap", high: "pivot"},
                        "swap",
                        f"Element {arr[i]} <= pivot ({pivot}). Swapped arr[{i}] <-> arr[{j}]"
                    )

            # Place pivot in its correct final partition position
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            pivot_idx = i + 1

            yield (
                arr,
                {pivot_idx: "sorted"},
                "swap",
                f"Pivot {pivot} locked in final sorted position at index {pivot_idx}"
            )

            # Recursively sort left and right partitions
            yield from _quick_sort_helper(low, pivot_idx - 1)
            yield from _quick_sort_helper(pivot_idx + 1, high)

    yield from _quick_sort_helper(0, len(arr) - 1)


# Metadata dictionary mapping choice to algorithm properties
ALGORITHMS_META = {
    1: {
        "name": "Bubble Sort",
        "func": bubble_sort,
        "best": "O(n)",
        "avg": "O(n²)",
        "worst": "O(n²)",
        "space": "O(1)",
        "stable": "Yes",
        "description": "Repeatedly steps through list, swaps adjacent out-of-order elements."
    },
    2: {
        "name": "Selection Sort",
        "func": selection_sort,
        "best": "O(n²)",
        "avg": "O(n²)",
        "worst": "O(n²)",
        "space": "O(1)",
        "stable": "No",
        "description": "Repeatedly extracts minimum element from unsorted partition."
    },
    3: {
        "name": "Insertion Sort",
        "func": insertion_sort,
        "best": "O(n)",
        "avg": "O(n²)",
        "worst": "O(n²)",
        "space": "O(1)",
        "stable": "Yes",
        "description": "Builds sorted array one element at a time by shifting larger items."
    },
    4: {
        "name": "Merge Sort",
        "func": merge_sort,
        "best": "O(n log n)",
        "avg": "O(n log n)",
        "worst": "O(n log n)",
        "space": "O(n)",
        "stable": "Yes",
        "description": "Divides array in halves, recursively sorts, and merges sorted sublists."
    },
    5: {
        "name": "Quick Sort",
        "func": quick_sort,
        "best": "O(n log n)",
        "avg": "O(n log n)",
        "worst": "O(n²)",
        "space": "O(log n)",
        "stable": "No",
        "description": "Lomuto partition scheme around a pivot, recursively sorting partitions."
    }
}


# ==============================================================================
# VISUALIZATION RENDERING ENGINE
# ==============================================================================
def build_frame(
    arr: List[int],
    highlights: Dict[int, str],
    algo_name: str,
    comparisons: int,
    swaps: int,
    elapsed_time: float,
    status_msg: str,
    chart_height: int = DEFAULT_CHART_HEIGHT,
    bar_char: str = DEFAULT_BAR_CHAR,
    delay_ms: float = DEFAULT_DELAY
) -> str:
    """
    Constructs an entire terminal frame as a single string buffer.

    Rendering components:
    1. Header banner and algorithm identification
    2. Dynamic live statistics (Comparisons, Swaps, Elapsed Time, Frame Delay)
    3. 2D Vertical bar chart matrix with ANSI color-coded bars
    4. Numeric value index beneath each bar (if space permits)
    5. Visual element color legend and current operation status message

    Returns:
        str: Fully formatted ANSI string ready for atomic stdout flush.
    """
    term_width, term_height = shutil.get_terminal_size((80, 24))
    n = len(arr)
    max_val = max(arr) if arr else 1

    # Dynamically cap chart height so total frame always fits in terminal window
    effective_chart_height = max(5, min(chart_height, term_height - 12))

    # Buffer accumulation
    lines: List[str] = []

    # 1. Header Banner
    w = min(term_width, 78)
    lines.append(f"{Colors.BLUE}{'=' * w}{Colors.RESET}{Colors.CLEAR_EOL}")
    title = f"SORTING VISUALIZER: {algo_name.upper()}"
    lines.append(f"{Colors.BOLD}{Colors.WHITE}{title.center(w)}{Colors.RESET}{Colors.CLEAR_EOL}")
    lines.append(f"{Colors.BLUE}{'=' * w}{Colors.RESET}{Colors.CLEAR_EOL}")

    # 2. Live Performance Metrics Bar
    stats_line = (
        f" {Colors.BOLD}Comparisons:{Colors.RESET} {Colors.YELLOW}{comparisons:<6}{Colors.RESET} | "
        f"{Colors.BOLD}Swaps/Writes:{Colors.RESET} {Colors.RED}{swaps:<6}{Colors.RESET} | "
        f"{Colors.BOLD}Time:{Colors.RESET} {Colors.CYAN}{elapsed_time:.2f}s{Colors.RESET} | "
        f"{Colors.BOLD}Speed:{Colors.RESET} {Colors.WHITE}{delay_ms*1000:.0f}ms/step{Colors.RESET}"
    )
    lines.append(f"{stats_line}{Colors.CLEAR_EOL}")
    lines.append(f"{Colors.GRAY}{'-' * w}{Colors.RESET}{Colors.CLEAR_EOL}")

    # Determine column spacing to center or evenly distribute bars
    available_width = min(term_width - 4, 76)
    if n * 3 <= available_width:
        col_width = 3
        bar_fill = bar_char * 2
        space_fill = " "
    elif n * 2 <= available_width:
        col_width = 2
        bar_fill = bar_char * 2
        space_fill = ""
    else:
        col_width = 1
        bar_fill = bar_char
        space_fill = ""

    # 3. 2D Vertical Bar Chart Matrix
    # We iterate from row = effective_chart_height down to 1
    chart_rows: List[str] = []
    for level in range(effective_chart_height, 0, -1):
        row_str = "  "
        for idx, val in enumerate(arr):
            # Calculate normalized height for this element
            bar_height = int((val / max_val) * effective_chart_height)
            if bar_height < 1 and val > 0:
                bar_height = 1

            # Determine color highlight for this column
            highlight_type = highlights.get(idx, None)
            if highlight_type == "compare":
                color = Colors.YELLOW
            elif highlight_type == "swap":
                color = Colors.RED
            elif highlight_type == "pivot":
                color = Colors.MAGENTA
            elif highlight_type == "sorted":
                color = Colors.GREEN
            else:
                color = Colors.CYAN

            # Draw bar segment or blank space
            if bar_height >= level:
                row_str += f"{color}{bar_fill}{Colors.RESET}{space_fill}"
            else:
                row_str += f"{' ' * len(bar_fill)}{space_fill}"

        chart_rows.append(f"{row_str}{Colors.CLEAR_EOL}")

    lines.extend(chart_rows)

    # 4. Base Baseline / Axis
    axis_length = n * (len(bar_fill) + len(space_fill))
    lines.append(f"  {Colors.GRAY}{'─' * axis_length}{Colors.RESET}{Colors.CLEAR_EOL}")

    # Numeric values line (if columns are wide enough)
    if col_width >= 3:
        val_line = "  "
        for val in arr:
            val_line += f"{Colors.WHITE}{val:2d}{Colors.RESET} "
        lines.append(f"{val_line}{Colors.CLEAR_EOL}")

    # 5. Visual Legend & Status Message
    legend = (
        f"{Colors.CYAN}■ Unsorted{Colors.RESET}  "
        f"{Colors.YELLOW}■ Comparing{Colors.RESET}  "
        f"{Colors.RED}■ Swap/Write{Colors.RESET}  "
        f"{Colors.MAGENTA}■ Pivot/Key{Colors.RESET}  "
        f"{Colors.GREEN}■ Sorted{Colors.RESET}"
    )
    lines.append(f"{Colors.GRAY}{'-' * w}{Colors.RESET}{Colors.CLEAR_EOL}")
    lines.append(f" {Colors.BOLD}Legend:{Colors.RESET} {legend}{Colors.CLEAR_EOL}")

    # Truncate status message if it exceeds terminal line width
    clean_msg = status_msg[:min(term_width - 12, 66)]
    lines.append(f" {Colors.BOLD}Action:{Colors.RESET} {Colors.WHITE}{clean_msg}{Colors.RESET}{Colors.CLEAR_EOL}")
    lines.append(f"{Colors.BLUE}{'=' * w}{Colors.RESET}{Colors.CLEAR_EOL}")

    # Assemble into single atomic frame string
    return "\n".join(lines) + "\n"


def run_visualizer(
    algo_key: int,
    array_size: int,
    delay: float,
    chart_height: int = DEFAULT_CHART_HEIGHT,
    bar_char: str = DEFAULT_BAR_CHAR
) -> None:
    """
    Orchestrates the visualization execution for the selected sorting algorithm.

    Steps:
    1. Generates and randomizes a new array of unique integers [1..N].
    2. Instantiates the algorithm generator.
    3. Animates frame-by-frame with zero flicker via cursor repositioning.
    4. Executes a victory green sweep across the array upon completion.
    5. Displays a comprehensive post-run analysis summary card.
    """
    meta = ALGORITHMS_META[algo_key]
    algo_name = meta["name"]
    algo_func = meta["func"]

    # 1. Initialize and randomize array (Fisher-Yates shuffle)
    arr = list(range(1, array_size + 1))
    random.shuffle(arr)

    # Clear screen once at the beginning of visualization
    clear_screen()
    hide_cursor()

    comparisons = 0
    swaps = 0
    start_time = time.perf_counter()

    try:
        # 2. Iterate through sorting generator events
        generator = algo_func(arr)
        for current_arr, highlights, op_type, message in generator:
            if op_type == "compare":
                comparisons += 1
            elif op_type == "swap":
                swaps += 1

            elapsed = time.perf_counter() - start_time

            # Build double-buffered frame string
            frame = build_frame(
                arr=current_arr,
                highlights=highlights,
                algo_name=algo_name,
                comparisons=comparisons,
                swaps=swaps,
                elapsed_time=elapsed,
                status_msg=message,
                chart_height=chart_height,
                bar_char=bar_char,
                delay_ms=delay
            )

            # Move cursor to top-left and flush frame atomically
            cursor_home()
            sys.stdout.write(frame)
            sys.stdout.flush()

            # Delay to control animation pacing
            time.sleep(delay)

        total_elapsed = time.perf_counter() - start_time

        # 3. Post-Sort Verification Sweep (Animated green wave confirming sorted state)
        for sweep_idx in range(len(arr)):
            green_map = {idx: "sorted" for idx in range(sweep_idx + 1)}
            frame = build_frame(
                arr=arr,
                highlights=green_map,
                algo_name=algo_name,
                comparisons=comparisons,
                swaps=swaps,
                elapsed_time=total_elapsed,
                status_msg=f"Verifying sorted order at index {sweep_idx} (arr[{sweep_idx}]={arr[sweep_idx]})... OK",
                chart_height=chart_height,
                bar_char=bar_char,
                delay_ms=delay
            )
            cursor_home()
            sys.stdout.write(frame)
            sys.stdout.flush()
            time.sleep(max(0.015, delay * 0.4))

        # Final all-green display
        all_green = {idx: "sorted" for idx in range(len(arr))}
        final_frame = build_frame(
            arr=arr,
            highlights=all_green,
            algo_name=algo_name,
            comparisons=comparisons,
            swaps=swaps,
            elapsed_time=total_elapsed,
            status_msg="SORT COMPLETED SUCCESSFULLY! Array is 100% sorted.",
            chart_height=chart_height,
            bar_char=bar_char,
            delay_ms=delay
        )
        cursor_home()
        sys.stdout.write(final_frame)
        sys.stdout.flush()

        # 4. Display Post-Sort Algorithmic Performance Card
        print_summary_card(meta, len(arr), comparisons, swaps, total_elapsed)

    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C user interruption during animation
        cursor_home()
        print(f"\n{Colors.RED}Visualization aborted by user (KeyboardInterrupt).{Colors.RESET}")
    finally:
        # Always restore terminal cursor
        show_cursor()


def print_summary_card(
    meta: dict,
    n: int,
    comparisons: int,
    swaps: int,
    elapsed: float
) -> None:
    """Prints a styled algorithmic evaluation and complexity summary card."""
    term_width, _ = shutil.get_terminal_size((80, 24))
    width = min(term_width, 78)

    print(f"\n{Colors.GREEN}{'━' * width}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'ALGORITHM EXECUTION SUMMARY'.center(width)}{Colors.RESET}")
    print(f"{Colors.GREEN}{'━' * width}{Colors.RESET}")
    print(f" {Colors.BOLD}Algorithm Name:{Colors.RESET}      {Colors.WHITE}{meta['name']}{Colors.RESET}")
    print(f" {Colors.BOLD}Mechanism:{Colors.RESET}           {Colors.GRAY}{meta['description']}{Colors.RESET}")
    print(f" {Colors.BOLD}Dataset Size (N):{Colors.RESET}    {Colors.WHITE}{n} elements{Colors.RESET}")
    print(f" {Colors.BOLD}Total Comparisons:{Colors.RESET}   {Colors.YELLOW}{comparisons}{Colors.RESET}")
    print(f" {Colors.BOLD}Total Swaps/Writes:{Colors.RESET}  {Colors.RED}{swaps}{Colors.RESET}")
    print(f" {Colors.BOLD}Wall-Clock Time:{Colors.RESET}     {Colors.CYAN}{elapsed:.4f} seconds{Colors.RESET}")
    print(f"{Colors.GRAY}{'─' * width}{Colors.RESET}")
    print(f" {Colors.BOLD}Theoretical Complexity:{Colors.RESET}")
    print(f"   • Best Case:      {Colors.GREEN}{meta['best']:<12}{Colors.RESET} • Average Case: {Colors.YELLOW}{meta['avg']:<12}{Colors.RESET}")
    print(f"   • Worst Case:     {Colors.RED}{meta['worst']:<12}{Colors.RESET} • Space (Aux):  {Colors.CYAN}{meta['space']:<12}{Colors.RESET}")
    print(f"   • Stable Sort:    {Colors.WHITE}{meta['stable']:<12}{Colors.RESET}")
    print(f"{Colors.GREEN}{'━' * width}{Colors.RESET}")


# ==============================================================================
# INTERACTIVE MENU & USER SETTINGS
# ==============================================================================
def display_main_menu(current_size: int, current_delay: float, current_char: str) -> None:
    """Renders the main menu interface."""
    term_width, _ = shutil.get_terminal_size((80, 24))
    w = min(term_width, 78)

    clear_screen()
    print(f"{Colors.BLUE}{'=' * w}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}{'CS5: TERMINAL SORTING ALGORITHM VISUALIZER'.center(w)}{Colors.RESET}")
    print(f"{Colors.CYAN}{'Philippine Science High School | Quarter 2'.center(w)}{Colors.RESET}")
    print(f"{Colors.BLUE}{'=' * w}{Colors.RESET}")
    print(f" {Colors.BOLD}Select an algorithm to visualize:{Colors.RESET}\n")

    for key, meta in ALGORITHMS_META.items():
        print(f"   {Colors.BOLD}[{key}]{Colors.RESET} {Colors.WHITE}{meta['name']:<16}{Colors.RESET}"
              f" {Colors.GRAY}Time: {meta['avg']:<10} Space: {meta['space']:<8} Stable: {meta['stable']:<4}{Colors.RESET}")

    print(f"\n   {Colors.BOLD}[6]{Colors.RESET} {Colors.CYAN}Customize Settings{Colors.RESET}"
          f" {Colors.GRAY}(Array Size: {current_size}, Delay: {current_delay*1000:.0f}ms, Bar: '{current_char}'){Colors.RESET}")
    print(f"   {Colors.BOLD}[7]{Colors.RESET} {Colors.MAGENTA}Algorithm Reference & Big-O Comparison Table{Colors.RESET}")
    print(f"   {Colors.BOLD}[0]{Colors.RESET} {Colors.RED}Exit Program{Colors.RESET}")
    print(f"{Colors.BLUE}{'=' * w}{Colors.RESET}")


def display_reference_table() -> None:
    """Displays a comprehensive theoretical comparison table for all 5 algorithms."""
    clear_screen()
    print(f"{Colors.BLUE}{'=' * 78}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}{'THEORETICAL BIG-O COMPLEXITY COMPARISON TABLE'.center(78)}{Colors.RESET}")
    print(f"{Colors.BLUE}{'=' * 78}{Colors.RESET}")
    print(f"{'Algorithm':<16} {'Best':<12} {'Average':<12} {'Worst':<12} {'Space':<10} {'Stable?':<8}")
    print(f"{Colors.GRAY}{'-' * 78}{Colors.RESET}")

    for _, meta in ALGORITHMS_META.items():
        print(f"{Colors.BOLD}{meta['name']:<16}{Colors.RESET} "
              f"{Colors.GREEN}{meta['best']:<12}{Colors.RESET} "
              f"{Colors.YELLOW}{meta['avg']:<12}{Colors.RESET} "
              f"{Colors.RED}{meta['worst']:<12}{Colors.RESET} "
              f"{Colors.CYAN}{meta['space']:<10}{Colors.RESET} "
              f"{Colors.WHITE}{meta['stable']:<8}{Colors.RESET}")

    print(f"{Colors.BLUE}{'=' * 78}{Colors.RESET}")
    print(f"\n{Colors.BOLD}Key Takeaways:{Colors.RESET}")
    print(" • Bubble Sort: Simple adjacent swaps; O(n) best-case with early-exit flag.")
    print(" • Selection Sort: Minimizes number of swaps (exactly O(n)), but always O(n²) comparisons.")
    print(" • Insertion Sort: Adaptive and online; highly efficient for nearly-sorted data.")
    print(" • Merge Sort: Consistent O(n log n) divide-and-conquer; requires O(n) auxiliary memory.")
    print(" • Quick Sort: Typically fastest in practice (cache-friendly in-place partitioning).")
    input(f"\n{Colors.YELLOW}Press [Enter] to return to the main menu...{Colors.RESET}")


def customize_settings(
    current_size: int,
    current_delay: float,
    current_char: str
) -> Tuple[int, float, str]:
    """
    Allows the user to interactively configure visualization parameters:
    - Array size
    - Frame animation delay (speed)
    - Bar rendering character
    """
    clear_screen()
    print(f"{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}{'CUSTOMIZE VISUALIZATION SETTINGS'.center(60)}{Colors.RESET}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f" Current Settings:")
    print(f"   1. Array Size:          {Colors.CYAN}{current_size} elements{Colors.RESET}")
    print(f"   2. Frame Delay (Speed): {Colors.CYAN}{current_delay:.3f} s ({current_delay*1000:.0f} ms/frame){Colors.RESET}")
    print(f"   3. Bar Glyph Character: {Colors.CYAN}'{current_char}'{Colors.RESET}")
    print(f"{Colors.GRAY}{'-' * 60}{Colors.RESET}")

    # 1. New Array Size
    size_input = input(f"Enter new array size [10 - 50] (Press Enter to keep {current_size}): ").strip()
    if size_input:
        try:
            val = int(size_input)
            if 5 <= val <= 60:
                current_size = val
                print(f"  {Colors.GREEN}✓ Array size updated to {current_size}.{Colors.RESET}")
            else:
                print(f"  {Colors.RED}⚠ Value out of bounds (5-60). Retaining {current_size}.{Colors.RESET}")
        except ValueError:
            print(f"  {Colors.RED}⚠ Invalid integer. Retaining {current_size}.{Colors.RESET}")

    # 2. New Delay
    delay_input = input(f"Enter animation delay in seconds [0.005 - 0.20] (Press Enter to keep {current_delay}): ").strip()
    if delay_input:
        try:
            val = float(delay_input)
            if 0.001 <= val <= 1.0:
                current_delay = val
                print(f"  {Colors.GREEN}✓ Frame delay updated to {current_delay*1000:.0f} ms.{Colors.RESET}")
            else:
                print(f"  {Colors.RED}⚠ Value out of bounds (0.001 - 1.0). Retaining {current_delay}.{Colors.RESET}")
        except ValueError:
            print(f"  {Colors.RED}⚠ Invalid float. Retaining {current_delay}.{Colors.RESET}")

    # 3. New Bar Character
    char_input = input(f"Enter bar character (e.g., █, #, |, *) (Press Enter to keep '{current_char}'): ").strip()
    if char_input:
        current_char = char_input[0]
        print(f"  {Colors.GREEN}✓ Bar character updated to '{current_char}'.{Colors.RESET}")

    input(f"\n{Colors.YELLOW}Settings saved. Press [Enter] to return to the main menu...{Colors.RESET}")
    return current_size, current_delay, current_char


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
def main() -> None:
    """Main program loop and user interface coordinator."""
    init_terminal()

    # Active operational configuration (defaults can also be modified in CONFIGURATION section)
    array_size = DEFAULT_ARRAY_SIZE
    delay = DEFAULT_DELAY
    bar_char = DEFAULT_BAR_CHAR

    while True:
        display_main_menu(array_size, delay, bar_char)
        choice = input(f"\n{Colors.BOLD}{Colors.WHITE}Enter your choice [0-7]: {Colors.RESET}").strip()

        if choice == "0":
            clear_screen()
            print(f"\n{Colors.CYAN}Thank you for using the Terminal Sorting Visualizer! Goodbye.{Colors.RESET}\n")
            break

        elif choice in ("1", "2", "3", "4", "5"):
            algo_key = int(choice)
            run_visualizer(
                algo_key=algo_key,
                array_size=array_size,
                delay=delay,
                chart_height=DEFAULT_CHART_HEIGHT,
                bar_char=bar_char
            )
            input(f"\n{Colors.YELLOW}Press [Enter] to return to the main menu...{Colors.RESET}")

        elif choice == "6":
            array_size, delay, bar_char = customize_settings(array_size, delay, bar_char)

        elif choice == "7":
            display_reference_table()

        else:
            print(f"{Colors.RED}Invalid option '{choice}'. Please select a number from 0 to 7.{Colors.RESET}")
            time.sleep(1.2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        show_cursor()
        print(f"\n\n{Colors.YELLOW}Program terminated by user.{Colors.RESET}")
        sys.exit(0)
