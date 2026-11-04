# 🎬 Sorting Algorithm Visualizer (`Vis.py`) — Walkthrough & Presentation Script

**Course:** CS5: Data Structures and Algorithms (Quarter 2)  
**School:** Philippine Science High School — Western Visayas Campus  
**Project:** Terminal-Based Sorting Algorithm Visualizer (`Vis.py`)  
**Estimated Time:** ~5 to 7 minutes  

---

## 📋 Pre-Recording / Pre-Defense Checklist

Before starting your recording or live demonstration:
1. **Terminal Setup:**
   - Open PowerShell, Windows Terminal, or VS Code integrated terminal.
   - Recommended window size: At least **80 columns wide** and **25–30 rows tall**.
   - Zoom in slightly (`Ctrl + +` or adjust font size) so the ASCII stars and colored text are crisp on screen.
2. **Directory Check:**
   - Ensure your current working directory is `c:\Users\LENOVO\CS5\Q2`.
   - Test command before recording: `python Vis.py`.
3. **Audio / Mic Check:**
   - Speak clearly and at a steady, relaxed pace.

---

## ⏱️ Step-by-Step Walkthrough Script

---

### Segment 1: Introduction & Project Overview (0:00 – 0:45)

| Time | What to Do on Screen | Spoken Script (What to Say) |
|---|---|---|
| **0:00** | Have the code file `Vis.py` open in VS Code showing the top docstring header. | *"Good day, Sir Gerald and classmates! Today I'll be walking you through my project for CS5 Quarter 2: an interactive, terminal-based Sorting Algorithm Visualizer written in Python."* |
| **0:20** | Scroll through the initial comments showing the README and algorithm list. | *"The goal of this project is to take abstract sorting algorithms and turn them into an intuitive, step-by-step visual demonstration right inside the terminal. Instead of relying on heavy third-party GUI libraries, it renders pure vertical ASCII star histograms with ANSI color highlights and a controlled 0.5-second delay per step."* |
| **0:35** | Hover over the 5 algorithms listed in the docstring. | *"It implements all five required canonical algorithms: Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, and Quick Sort."* |

---

### Segment 2: Code Architecture & Disclaimers / Citations (0:45 – 1:45)

| Time | What to Do on Screen | Spoken Script (What to Say) |
|---|---|---|
| **0:45** | Scroll down to the `IMPORTS & CITATIONS / DISCLAIMERS` section (around lines 55–100). | *"Before running the demo, let's look at the structure and documentation. To practice proper academic integrity, I've explicitly documented all my external references and Stack Overflow citations right under the imports."* |
| **1:05** | Point out the links for `os`, `sys`, ANSI colors, and screen re-drawing. | *"For example, the ANSI escape codes used for color formatting and the virtual terminal setup on Windows were adapted from discussions on Stack Overflow. The canonical algorithmic logic for the five sorts references GeeksforGeeks."* |
| **1:25** | Point out the `draw_bars()` function and explain why `yield` is not used. | *"One design decision I made was to keep the code clean and readable by avoiding complex generator pipelines and `yield` statements. Instead, each sorting function simply calls a helper function called `draw_bars()` whenever a comparison or a swap occurs. This keeps the logic modular, direct, and very easy to trace."* |
| **1:40** | Highlight the constants: `DELAY = 0.5`, `MAX_ELEMENTS = 10`, `STAR_CHAR = "*"`. | *"At the top, we have our parameters. The delay is set to 0.5 seconds per step, the maximum elements are capped at 10 to fit cleanly in standard console windows, and the star glyph is set to a classic asterisk."* |

---

### Segment 3: Live Demo — Bubble Sort & Early Exit (1:45 – 3:15)

| Time | What to Do on Screen | Spoken Script (What to Say) |
|---|---|---|
| **1:45** | Open the terminal and type:  <br>`python Vis.py`<br>Press `Enter`. | *"Now let's launch the program with `python Vis.py`."* |
| **1:55** | Terminal displays the welcome banner and prompt:  <br>`Enter number of RANDOMIZED elements to sort (1 to 10):`  <br>Type `5` and press `Enter`. | *"First, the program prompts us for the number of randomized elements to use, up to 10. Let's enter `5`."* |
| **2:05** | Point to the printed array (e.g., `[9, 4, 12, 2, 7]`). | *"The program uses `random.sample` to generate 5 unique integers between 1 and 14. Notice that because they are small positive integers, each number's value directly matches its vertical height in stars! For instance, a value of 9 has literally 9 stars stacked vertically."* |
| **2:15** | Prompt shows:  <br>`Enter algorithm choice (1-5):`  <br>Type `1` for Bubble Sort and press `Enter`. | *"Next, we are prompted for the sorting algorithm. Let's start with option `[1]` for Bubble Sort."* |
| **2:25** | The screen clears and the 0.5s animation begins.  <br>Point your cursor to the colors as they change. | *"The visualizer starts animating with our 0.5-second delay. Notice what's happening on screen:*  <br>• **Yellow stars:** *Indicate the two adjacent elements currently being compared.*  <br>• **Red stars:** *Flash when elements are out of order and being swapped.*  <br>• **Green stars:** *Represent elements that have locked into their final sorted positions at the end of each pass.*  <br>• **Live Metrics:** *The header tracks our current step count, comparisons, and swaps in real time.*  <br>• **Action Line:** *The bottom status bar explicitly tells us what the algorithm is thinking—like 'Comparing arr[1] and arr[2]' or 'Swapped out-of-order elements'."* |
| **2:55** | The sort completes. The whole chart turns green and the summary card appears. | *"When the sort finishes, the entire array turns green to celebrate completion. Because Bubble Sort tracks a `swapped` boolean flag, if an entire pass finishes with zero swaps, it triggers an early exit in $O(n)$ time. Here is the post-sort summary card showing total comparisons, swaps, and the verified ascending array."* |

---

### Segment 4: Live Demo — Quick Sort & Play-Again Loop (3:15 – 4:45)

| Time | What to Do on Screen | Spoken Script (What to Say) |
|---|---|---|
| **3:15** | Prompt asks:  <br>`Would you like to sort another array? (y/n):`  <br>Type `y` and press `Enter`. | *"Now the program asks if we want to go again. I'll type `y`."* |
| **3:25** | Enter `6` for the number of elements.  <br>Then enter `5` for **Quick Sort**. | *"Let's test Quick Sort with 6 elements."* |
| **3:35** | Quick Sort animation runs. Point out the Magenta pivot. | *"Quick Sort uses the canonical Lomuto partitioning scheme. Notice the **Magenta** star column—that's our pivot, chosen as the rightmost element in the current range. The algorithm scans from left to right, comparing each element against the pivot (in Yellow), swapping smaller items to the left (in Red), and finally placing the pivot into its permanent sorted position (in Green). Then it recursively partitions the remaining sub-arrays."* |
| **4:15** | Sort finishes. Prompt asks:  <br>`Would you like to sort another array? (y/n):`  <br>Type `n` and press `Enter`. | *"Once Quick Sort finishes, it displays the final summary. When we enter `n`, the program prints a polite farewell message and exits cleanly back to the terminal prompt."* |

---

### Segment 5: Rubrics & Technical Verification (4:45 – 5:45)

| Time | What to Do on Screen | Spoken Script (What to Say) |
|---|---|---|
| **4:45** | Switch back to the code editor in `Vis.py`. Scroll to functions `selection_sort`, `insertion_sort`, `merge_sort`. | *"To recap how this implementation satisfies the assignment rubrics:*  <br>1. **Aesthetic & Intuitive Visualization:** *The vertical star bars provide an immediate visual gauge of magnitude. With centered values, indices, and color roles (Yellow, Red, Magenta, Green), comparisons and swaps are immediately clear.*  <br>2. **All 5 Canonical Algorithms:** *Bubble, Selection, Insertion, Merge, and Quick Sort are all implemented following standard canonical logic without shortcuts, and they correctly sort all edge cases.*  <br>3. **Flawless Display & Terminal Clearing:** *Instead of repeatedly calling `os.system('cls')` which causes noticeable screen tearing and flashing, the program uses the ANSI cursor-home escape sequence `\033[H` to overwrite the frame in place. It also enables virtual terminal processing for Windows consoles and reconfigures UTF-8 encoding.*  <br>4. **Modular Code & In-Program Documentation:** *Every sorting algorithm and utility is encapsulated into clean, readable functions with helpful docstrings, comments, and parameter controls."* |

---

### Segment 6: Conclusion (5:45 – 6:00)

| Time | What to Do on Screen | Spoken Script (What to Say) |
|---|---|---|
| **5:45** | Return to the terminal showing the clean exit. | *"That concludes the walkthrough of the Terminal Sorting Algorithm Visualizer. Thank you very much for listening, and I'd be glad to answer any questions or demonstrate any specific sorting cases!"* |

---

## 💡 Anticipated Defense Questions & Answers (Cheat Sheet)

If your teacher or panel asks follow-up questions during your defense, here are concise answers:

### Q1: "Why did you use direct calls to `draw_bars()` instead of Python generators with `yield`?"
> **Answer:**  
> *"Using generators with `yield` adds unnecessary syntactic overhead (`Generator[Tuple[...]]`) and makes the sorting logic harder to read. By passing the array and the active indices directly to a modular `draw_bars()` helper function, the code is much simpler, more beginner-friendly, and immediately shows the cause-and-effect of each comparison and swap without decoupling the execution context."*

### Q2: "How does your terminal stay smooth and flicker-free without standard `cls`?"
> **Answer:**  
> *"Calling `os.system('cls')` spawns a brand new OS process on every frame, which clears the entire screen buffer and causes noticeable black-screen flashing. Instead, I clear the screen once at the start, hide the blinking cursor with `\033[?25l`, and on every step use the ANSI escape code `\033[H` to reposition the cursor to row 1, column 1. The whole frame is written in a single atomic `sys.stdout.write()` call, completely eliminating screen tearing."*

### Q3: "How does Bubble Sort achieve $O(n)$ best-case performance in your program?"
> **Answer:**  
> *"Standard Bubble Sort takes $O(n^2)$ even on a sorted array because it continues looping. My implementation includes an optimized `swapped = False` boolean flag inside each outer pass. If an entire pass completes without a single adjacent swap, `swapped` remains `False`, meaning all elements are in order, and the program executes an early `break` after just $n-1$ comparisons."*

### Q4: "Which Quick Sort partition scheme did you implement, and what is its worst-case complexity?"
> **Answer:**  
> *"I implemented the canonical **Lomuto partition scheme**, which selects the rightmost element as the pivot (`arr[high]`) and uses an index pointer `i` to collect elements smaller than or equal to the pivot. Its average time complexity is $O(n \log n)$, but if the array is already sorted or reverse-sorted, it can degrade to $O(n^2)$ because the partitions become highly unbalanced ($1$ and $n-1$)."*

### Q5: "Is your Merge Sort stable? Why?"
> **Answer:**  
> *"Yes, it is stable. In the merge subroutine, when comparing elements from the left and right halves:  
> `if left_copy[p1] <= right_copy[p2]:`  
> The use of `<=` guarantees that if two elements have equal values, the one from the left half is placed first into the merged array, preserving their original relative order."*

### Q6: "How does the random value range handle changes to MAX_ELEMENTS?"
> **Answer:**  
> *"Instead of hardcoding a fixed range, the random population pool dynamically scales with `max(15, max(n, MAX_ELEMENTS) + 5)`. This ensures that even if `MAX_ELEMENTS` is increased to 20 or 30, `random.sample()` will never throw a `ValueError` from a depleted pool. Furthermore, `draw_bars()` automatically normalizes bar heights to a maximum of 14 terminal rows if elements exceed 14, preventing vertical screen overflow."*

---

*Walkthrough script prepared for CS5 Quarter 2 Machine Problem / Alternative Assessment.*

