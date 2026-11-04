# 🖥️ Under the Hood: Terminal Control & Colors in Python

**A Beginner-Friendly Guide to the "Magic" Used in `Vis.py`**  
*Philippine Science High School — CS5 (Quarter 2)*

---

## 📌 Introduction

If you've mostly written standard console programs using `print()` and `input()`, `Vis.py` might feel like it's doing something impossible:
- How does text change color without installing third-party packages like `colorama` or `curses`?
- How does the screen update smoothly without flashing or flickering?
- Where did the blinking cursor go?
- What does weird-looking syntax like `\033[93m` or `\033[H` actually mean?

This guide breaks down every new concept used in `Vis.py` in plain English, explains how it works behind the scenes, and provides a handy cheat sheet you can use in future programming projects.

---

## 🎨 1. Terminal Colors: ANSI Escape Sequences

### What is an ANSI Escape Sequence?
A terminal (like Command Prompt, PowerShell, or the VS Code terminal) is essentially a text-based display screen. In the early days of computing, video terminals (like the famous **DEC VT100** from 1978) needed a way for computers to tell them:
> *"Don't print these next characters on screen; instead, treat them as a command to change text color, move the cursor, or clear the screen!"*

To do this, computer scientists created **Escape Sequences**. They all start with an **Escape character** (`ESC`), followed by a bracket `[`, some numbers/codes, and a command letter.

In Python strings, the Escape character is written as:
- `\033` (octal notation for character 27)
- or `\x1b` (hexadecimal notation for 27)

```
        Escape Character
              │
              ▼
            \033 [ 93 m
                 ▲  ▲ ▲
                 │  │ └── Command letter ('m' means "Select Graphic Rendition / Style")
                 │  └──── Parameter code (93 = Bright Yellow)
                 └─────── Bracket delimiter
```

When your terminal sees `\033[93m`, it stops printing characters as text, switches its internal pen color to **Bright Yellow**, and continues printing everything in yellow until told otherwise!

---

### The All-Important "Reset" Code (`\033[0m`)
ANSI codes are **sticky**. If you print:
```python
print("\033[91mHello world")
print("This is another line")
```
Both lines will be printed in red! In fact, your terminal prompt might stay red even after your Python program exits!

To prevent this, you **must** send the reset code:
```python
RESET = "\033[0m"
print(f"\033[91mHello world{RESET}")
print("Now I am normal white again!")
```

---

### Standard vs. High-Intensity (Bright) Colors

ANSI supports standard colors (30–37) and bright/high-intensity colors (90–97). In `Vis.py`, we use the **90-series** because they pop out much more vibrantly on modern dark-mode terminal screens:

| Color | Standard (Dimmer) | Bright / Bold (Used in `Vis.py`) | Role in `Vis.py` |
|---|---|---|---|
| **Red** | `\033[31m` | `\033[91m` | Swapping / Shifting elements |
| **Green** | `\033[32m` | `\033[92m` | Locked sorted elements |
| **Yellow** | `\033[33m` | `\033[93m` | Elements being compared |
| **Blue** | `\033[34m` | `\033[94m` | Borders and headers |
| **Magenta** | `\033[35m` | `\033[95m` | Pivot (Quick) / Key (Insertion) |
| **Cyan** | `\033[36m` | `\033[96m` | Default unsorted bars |
| **White** | `\033[37m` | `\033[97m` | Numeric values & status text |
| **Gray** | `\033[90m` | `\033[90m` | Subtle divider lines & indices |

---

## ⚡ 2. Flicker-Free Screen Animation

### The Beginner Problem: Why `os.system('cls')` Flickers
When beginners want to animate something in the terminal, they usually do this in a loop:
```python
# The flickering way (DO NOT DO THIS FOR ANIMATIONS):
while True:
    os.system("cls")  # or os.system("clear") on Mac/Linux
    draw_stuff()
    time.sleep(0.5)
```
If you run that, the terminal screen **flashes black** violently on every single frame! Why?
1. **Slow Process Creation:** `os.system("cls")` asks Windows to launch a completely new background process `cmd.exe`, run the `cls` binary, and terminate. Spawning a process takes 10–50 milliseconds.
2. **Buffer Blanking:** `cls` erases the entire terminal buffer to blank black pixels. Your eyes see that black screen before Python has time to print the next frame, causing an annoying strobe effect.

---

### The Professional Fix: Cursor Repositioning (`\033[H`)
Instead of clearing the screen, what if we just **move the cursor back to the very top-left corner (Row 1, Column 1)** and overwrite the existing characters with the new frame?

```
               \033[H  (Cursor Home)
                 │
                 ▼
          ┌─────────────┐
          │ *   *   *   │  <-- Existing frame
          │ 4   7   9   │
          └─────────────┘
                 │
                 ▼  (Cursor snaps to top-left instantly)
          ┌─────────────┐
          │ *   *       │  <-- Overwritten frame (zero delay!)
          │ 7   4   9   │
          └─────────────┘
```

The code in `Vis.py` does this:
```python
def cursor_home():
    sys.stdout.write("\033[H")
    sys.stdout.flush()
```
- `\033[H` tells the terminal: *"Move the typing cursor to row 1, column 1 without erasing anything."*
- Overwriting existing characters happens in microseconds directly in video memory. To the human eye, the animation looks like a smooth 60fps video!

---

### Preventing "Ghost" Characters with `\033[K`
What happens if Frame 1 prints a long status line:
`Action: Swapped out-of-order elements: arr[2] <-> arr[3]` (55 characters)

And Frame 2 prints a shorter status line:
`Action: Pass 2 done` (19 characters)

If you just overwrite it, the end of the old sentence would still be visible:
`Action: Pass 2 done-of-order elements: arr[2] <-> arr[3]` 😱!

To fix this, `Vis.py` appends `Colors.CLEAR_EOL` (`\033[K`) to the end of every line:
- `\033[K` means **"Clear from cursor position to the End Of the Line"**.
- It cleanly erases any leftover characters from the previous frame.

---

### Single Atomic Write Buffer
Instead of calling `print()` 20 times per frame, `Vis.py` builds the entire screen in memory as a single Python list of strings, joins them with `\n`, and sends them to the terminal in **one single write**:
```python
cursor_home()
sys.stdout.write("\n".join(lines) + "\n")
sys.stdout.flush()
```
`sys.stdout.flush()` forces Python's internal I/O buffer to immediately dump all characters to your monitor without waiting.

---

## 👁️ 3. Cursor Visibility Control (`\033[?25l` & `\033[?25h`)

Have you ever noticed that during the sort animation, the blinking cursor (`_` or `█`) isn't dancing around the screen?

Normally, as characters are printed, the cursor moves along with every character. During fast animations, this creates a distracting, jittery white box flickering all over the chart.

ANSI provides a simple command to turn the cursor off and on:
- `\033[?25l` (lowercase L): **Hide Cursor** (makes the cursor invisible).
- `\033[?25h`: **Show Cursor** (restores normal blinking cursor).

```python
def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()
```

### ⚠️ The Golden Rule of Cursor Hiding
If your program hides the cursor and then crashes (e.g., you press `Ctrl + C`), the cursor will **stay invisible** in your terminal window even after Python stops!

That is why `Vis.py` always uses `try ... finally`:
```python
try:
    hide_cursor()
    # run sorting animation...
finally:
    show_cursor()  # GUARANTEED to run even if an error or Ctrl+C happens!
```

---

## 🪟 4. The Windows ANSI "Gotcha" & `os.system("")`

On macOS and Linux, terminals have supported ANSI escape codes natively for decades. 

However, historically on older versions of Windows (Windows 7/8 and early Windows 10), Command Prompt and PowerShell did **not** enable ANSI codes by default. If you printed `\033[93m`, it would literally display ugly garbage like:
```text
←[93m* ←[0m
```

### The Magic Trick: `os.system("")`
In Python, calling `os.system("")` with an empty string forces the Windows OS kernel to initialize the console's virtual terminal processing flag (`ENABLE_VIRTUAL_TERMINAL_PROCESSING`). 

Once that single dummy call runs at the start of your program, Windows permanently enables ANSI color parsing for the rest of your session!

```python
def init_terminal():
    if os.name == "nt":   # 'nt' means Windows
        os.system("")     # Activates ANSI mode on Windows!
```

---

## 📊 5. How to Draw a Vertical Bar Chart in Text

Terminals only print from **top to bottom, left to right**. You cannot print column 1, then go back to the top and print column 2.

So how do we draw vertical bars like this?
```text
            *
    *       *
    *   *   *
  ------------
    2   1   3
```

### The Inverted Loop Strategy
We iterate **backwards** from the highest level down to level 1:

```python
# Suppose arr = [2, 1, 3], so max_h = 3

for level in range(3, 0, -1):  # level = 3, then 2, then 1
    row = ""
    for val in arr:
        if val >= level:
            row += "  * "  # Value is tall enough to reach this row!
        else:
            row += "    "  # Blank air space
    print(row)
```

Trace table:
- When `level = 3`:
  - `val = 2`: $2 \ge 3$ is `False` $\rightarrow$ prints `"    "`
  - `val = 1`: $1 \ge 3$ is `False` $\rightarrow$ prints `"    "`
  - `val = 3`: $3 \ge 3$ is `True`  $\rightarrow$ prints `"  * "`
  - *Result:* `        * `
- When `level = 2`:
  - `val = 2`: $2 \ge 2$ is `True`  $\rightarrow$ prints `"  * "`
  - `val = 1`: $1 \ge 2$ is `False` $\rightarrow$ prints `"    "`
  - `val = 3`: $3 \ge 2$ is `True`  $\rightarrow$ prints `"  * "`
  - *Result:* `  *     * `
- When `level = 1`:
  - All three values are $\ge 1$ $\rightarrow$ prints `"  *   *   * "`

Underneath the loop, we simply draw the baseline `----`, the numbers `2  1  3`, and the indices `[0][1][2]`.

---

## 📑 6. Quick Reference Cheat Sheet

Save this table for future programming machine problems:

| Concept / Action | Code | What It Does |
|---|---|---|
| **Reset Colors** | `\033[0m` | Reverts all text styling back to normal. |
| **Bright Red** | `\033[91m` | Changes text color to high-visibility red. |
| **Bright Green** | `\033[92m` | Changes text color to high-visibility green. |
| **Bright Yellow** | `\033[93m` | Changes text color to high-visibility yellow. |
| **Bright Blue** | `\033[94m` | Changes text color to high-visibility blue. |
| **Bright Magenta** | `\033[95m` | Changes text color to high-visibility purple/magenta. |
| **Bright Cyan** | `\033[96m` | Changes text color to high-visibility light blue/cyan. |
| **Bold Text** | `\033[1m` | Makes subsequent text bold. |
| **Move Cursor Home** | `\033[H` | Jumps cursor to row 1, col 1 (flicker-free updates). |
| **Erase to End of Line** | `\033[K` | Erases leftover characters on the current line. |
| **Hide Cursor** | `\033[?25l` | Hides blinking typing cursor. |
| **Show Cursor** | `\033[?25h` | Restores blinking typing cursor. |
| **Windows ANSI Fix** | `os.system("")` | Tells Windows CMD/PowerShell to process ANSI codes. |
| **Clear Terminal** | `os.system("cls" if os.name == "nt" else "clear")` | Full screen wipe across Windows, Mac, and Linux. |

