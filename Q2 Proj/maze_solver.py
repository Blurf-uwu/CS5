# maze_solver.py
# module 3 - solves a 2D maze using a stack to backtrack out of dead ends
#
# maze symbols:
#   '|' = wall
#   'S' = start
#   'E' = exit
#   '.' = open space you can walk on

from stack_adt import Stack

WALL = "|"
START = "S"
EXIT = "E"
OPEN = "."

# the order we try moving in: up, right, down, left
DIRECTIONS = [(-1, 0, "up"), (0, 1, "right"), (1, 0, "down"), (0, -1, "left")]

# a small maze to use as a default / demo
SAMPLE_MAZE = [
    "||||||||||",
    "|S...|.|.|",
    "|.||.|.|.|",
    "|.|..|.|.|",
    "|.|.||.|.|",
    "|...|..|.|",
    "|||.|.||.|",
    "|........|",
    "|.||||||E|",
    "||||||||||",
]


def make_grid(lines):
    """
    turns a list of strings into a 2D grid (list of lists of characters).
    blank lines get skipped. raises ValueError if the maze has bad characters
    or doesn't have exactly one 'S' and one 'E'.
    """
    grid = []
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        row = []
        for ch in line:
            if ch != WALL and ch != START and ch != EXIT and ch != OPEN:
                raise ValueError("maze has an invalid character: '" + ch + "' (only | . S E allowed)")
            row.append(ch)
        grid.append(row)

    if len(grid) == 0:
        raise ValueError("maze is empty")

    # count the starts and exits, there should be one of each
    starts = 0
    exits = 0
    for row in grid:
        for ch in row:
            if ch == START:
                starts = starts + 1
            elif ch == EXIT:
                exits = exits + 1
    if starts != 1:
        raise ValueError("maze needs exactly one 'S' (found " + str(starts) + ")")
    if exits != 1:
        raise ValueError("maze needs exactly one 'E' (found " + str(exits) + ")")

    return grid


def load_maze_from_file(filename):
    """reads a maze from a text file (one row per line) and returns the grid."""
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    return make_grid(lines)


def find_char(grid, target):
    """returns the (row, col) of the first spot in the grid that has target, or None."""
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == target:
                return (r, c)
    return None


def in_bounds(grid, r, c):
    """True if (r, c) is actually inside the grid. rows can be different lengths."""
    if r < 0 or r >= len(grid):
        return False
    if c < 0 or c >= len(grid[r]):
        return False
    return True


def solve_maze(grid):
    """
    tries to find a path from 'S' to 'E' using a stack.

    how it works:
      - push the start (row, col) onto the path stack
      - look at the top of the stack (where we are now)
      - if there's an open neighbor we haven't been to, push it (move there)
      - if every neighbor is a wall / out of bounds / already visited, then
        it's a dead end so we pop() to backtrack to the spot before
      - keep going until we reach 'E' or the stack is empty (no way out)

    returns (found, path, log)
      found - True if we got to the exit
      path  - list of (row, col) from start to exit (empty if not found)
      log   - list of strings describing every move, wall hit and backtrack
    """
    start = find_char(grid, START)
    end = find_char(grid, EXIT)

    path = Stack()
    visited = []      # every spot we've stepped on
    walls_hit = []    # walls we bumped into (only logged once each)
    log = []

    path.push(start)
    visited.append(start)
    log.append("start at " + str(start))

    while not path.isEmpty():
        current = path.peek()

        # made it out!
        if current == end:
            log.append("reached the exit at " + str(current))
            break

        r = current[0]
        c = current[1]
        moved = False

        for d in DIRECTIONS:
            nr = r + d[0]
            nc = c + d[1]
            name = d[2]

            if not in_bounds(grid, nr, nc):
                continue  # off the edge of the maze

            if grid[nr][nc] == WALL:
                # wall collision, can't go this way
                if (nr, nc) not in walls_hit:
                    walls_hit.append((nr, nc))
                    log.append("  wall at " + str((nr, nc)) + " going " + name + " from " + str(current))
                continue

            if (nr, nc) in visited:
                continue  # been here already, don't go in circles

            # found a new open spot so move there
            path.push((nr, nc))
            visited.append((nr, nc))
            log.append("move " + name + " to " + str((nr, nc)))
            moved = True
            break

        if not moved:
            # dead end, nothing new to try from here so backtrack
            dead = path.pop()
            if path.isEmpty():
                log.append("dead end at " + str(dead) + ", nothing left to backtrack to")
            else:
                log.append("dead end at " + str(dead) + ", backtrack (pop) to " + str(path.peek()))

    if path.isEmpty():
        log.append("no path to the exit :(")
        return (False, [], log)

    # pop everything off to get the path, it comes out backwards (exit first)
    backwards = []
    while not path.isEmpty():
        backwards.append(path.pop())

    final_path = []
    i = len(backwards) - 1
    while i >= 0:
        final_path.append(backwards[i])
        i = i - 1

    return (True, final_path, log)


def maze_to_string(grid, path=None):
    """
    makes a printable version of the maze. if a path is given, the open
    spots on the path get marked with '*'.
    """
    text = ""
    for r in range(len(grid)):
        line = ""
        for c in range(len(grid[r])):
            ch = grid[r][c]
            if path is not None and (r, c) in path and ch == OPEN:
                line = line + "*"
            else:
                line = line + ch
        text = text + line + "\n"
    return text
