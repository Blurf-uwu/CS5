# main.py
# module 4 - the menu you actually run, plus the test suite
# run it with:  python main.py

import os
import tempfile
import unittest

from stack_adt import Stack
from expr_processor import parChecker, infix_to_prefix, tokenize, check_infix
from maze_solver import (SAMPLE_MAZE, make_grid, load_maze_from_file,
                         solve_maze, maze_to_string, find_char)


# ---------------------------------------------------------------
# tests
# ---------------------------------------------------------------

class TestStack(unittest.TestCase):
    """tests for the Stack class in stack_adt.py"""

    def test_new_stack_is_empty(self):
        s = Stack()
        self.assertTrue(s.isEmpty())
        self.assertEqual(s.size(), 0)

    def test_push_changes_size(self):
        s = Stack()
        s.push(1)
        s.push(2)
        self.assertFalse(s.isEmpty())
        self.assertEqual(s.size(), 2)

    def test_lifo_order(self):
        # last one in should be the first one out
        s = Stack()
        s.push("a")
        s.push("b")
        s.push("c")
        self.assertEqual(s.pop(), "c")
        self.assertEqual(s.pop(), "b")
        self.assertEqual(s.pop(), "a")
        self.assertTrue(s.isEmpty())

    def test_peek_does_not_remove(self):
        s = Stack()
        s.push(5)
        s.push(10)
        self.assertEqual(s.peek(), 10)
        self.assertEqual(s.size(), 2)

    def test_pop_empty_raises(self):
        s = Stack()
        self.assertRaises(IndexError, s.pop)

    def test_peek_empty_raises(self):
        s = Stack()
        self.assertRaises(IndexError, s.peek)

    def test_pop_after_emptying_raises(self):
        s = Stack()
        s.push(1)
        s.pop()
        self.assertRaises(IndexError, s.pop)

    def test_can_hold_tuples(self):
        # the maze pushes (row, col) tuples so make sure that works
        s = Stack()
        s.push((1, 2))
        self.assertEqual(s.peek(), (1, 2))


class TestParChecker(unittest.TestCase):
    """tests for parChecker in expr_processor.py"""

    def test_balanced(self):
        self.assertTrue(parChecker("(A + B)"))
        self.assertTrue(parChecker("((A + B) * (C - D))"))
        self.assertTrue(parChecker("(()()())"))

    def test_no_parens_is_balanced(self):
        self.assertTrue(parChecker("A + B"))
        self.assertTrue(parChecker(""))

    def test_missing_close(self):
        self.assertFalse(parChecker("((A + B)"))
        self.assertFalse(parChecker("((("))

    def test_early_failure(self):
        # ')' comes before any '(' so pop on an empty stack -> fail early
        self.assertFalse(parChecker(")A + B("))
        self.assertFalse(parChecker("(A + B))"))
        self.assertFalse(parChecker(")"))

    def test_same_count_wrong_order(self):
        self.assertFalse(parChecker("())("))


class TestTokenize(unittest.TestCase):
    """tests for the tokenize and check_infix helpers"""

    def test_simple(self):
        self.assertEqual(tokenize("A+B"), ["A", "+", "B"])

    def test_spaces_and_multi_digit(self):
        self.assertEqual(tokenize(" 12 * (3 + 45) "), ["12", "*", "(", "3", "+", "45", ")"])

    def test_bad_character(self):
        self.assertRaises(ValueError, tokenize, "A $ B")

    def test_check_infix_good(self):
        check_infix(["(", "A", "+", "B", ")", "*", "C"])  # shouldn't raise

    def test_check_infix_bad(self):
        self.assertRaises(ValueError, check_infix, ["A", "+", "+", "B"])
        self.assertRaises(ValueError, check_infix, ["A", "+"])
        self.assertRaises(ValueError, check_infix, ["A", "B"])
        self.assertRaises(ValueError, check_infix, [])


class TestInfixToPrefix(unittest.TestCase):
    """tests for infix_to_prefix in expr_processor.py"""

    def test_basic(self):
        self.assertEqual(infix_to_prefix("A + B"), "+ A B")
        self.assertEqual(infix_to_prefix("A * B"), "* A B")

    def test_precedence(self):
        self.assertEqual(infix_to_prefix("A + B * C"), "+ A * B C")
        self.assertEqual(infix_to_prefix("A * B + C"), "+ * A B C")

    def test_parentheses(self):
        self.assertEqual(infix_to_prefix("(A + B) * C"), "* + A B C")

    def test_nested_parentheses(self):
        self.assertEqual(infix_to_prefix("((A + B) * (C - D)) ^ E"), "^ * + A B - C D E")
        self.assertEqual(infix_to_prefix("A * (B + (C - D))"), "* A + B - C D")

    def test_left_associative(self):
        # A - B - C means (A - B) - C
        self.assertEqual(infix_to_prefix("A - B - C"), "- - A B C")
        self.assertEqual(infix_to_prefix("A / B * C"), "* / A B C")

    def test_exponent(self):
        # ^ is the strongest and goes right to left, A ^ B ^ C = A ^ (B ^ C)
        self.assertEqual(infix_to_prefix("A ^ B ^ C"), "^ A ^ B C")
        self.assertEqual(infix_to_prefix("2 ^ 3 * 4"), "* ^ 2 3 4")
        self.assertEqual(infix_to_prefix("A + B * C ^ D - E"), "- + A * B ^ C D E")

    def test_numbers(self):
        self.assertEqual(infix_to_prefix("12 + 345"), "+ 12 345")

    def test_single_operand(self):
        self.assertEqual(infix_to_prefix("X"), "X")

    def test_unbalanced_raises(self):
        self.assertRaises(ValueError, infix_to_prefix, "(A + B")
        self.assertRaises(ValueError, infix_to_prefix, "A + B)")

    def test_invalid_raises(self):
        self.assertRaises(ValueError, infix_to_prefix, "A + * B")
        self.assertRaises(ValueError, infix_to_prefix, "")


class TestMaze(unittest.TestCase):
    """tests for maze_solver.py"""

    def check_path(self, grid, path):
        # helper - makes sure a path is actually legit
        self.assertEqual(path[0], find_char(grid, "S"))
        self.assertEqual(path[len(path) - 1], find_char(grid, "E"))
        for i in range(len(path)):
            r = path[i][0]
            c = path[i][1]
            self.assertNotEqual(grid[r][c], "|")  # never walks through a wall
            if i > 0:
                # each step should be exactly one square away
                pr = path[i - 1][0]
                pc = path[i - 1][1]
                self.assertEqual(abs(r - pr) + abs(c - pc), 1)

    def test_sample_maze_solves(self):
        grid = make_grid(SAMPLE_MAZE)
        found, path, log = solve_maze(grid)
        self.assertTrue(found)
        self.check_path(grid, path)

    def test_sample_maze_backtracks(self):
        # the sample maze has dead ends so there should be pops in the log
        grid = make_grid(SAMPLE_MAZE)
        found, path, log = solve_maze(grid)
        backtracks = 0
        for line in log:
            if "backtrack" in line:
                backtracks = backtracks + 1
        self.assertTrue(backtracks > 0)

    def test_wall_collisions_logged(self):
        grid = make_grid(SAMPLE_MAZE)
        found, path, log = solve_maze(grid)
        walls = 0
        for line in log:
            if "wall at" in line:
                walls = walls + 1
        self.assertTrue(walls > 0)

    def test_dead_end_then_exit(self):
        # going up first leads to a dead end, has to come back down
        grid = make_grid([
            "|||||",
            "|.|||",
            "|S..E",
            "|||||",
        ])
        found, path, log = solve_maze(grid)
        self.assertTrue(found)
        self.assertEqual(path, [(2, 1), (2, 2), (2, 3), (2, 4)])
        self.assertTrue((1, 1) not in path)  # the dead end got popped

    def test_no_path(self):
        grid = make_grid([
            "|||||",
            "|S|E|",
            "|||||",
        ])
        found, path, log = solve_maze(grid)
        self.assertFalse(found)
        self.assertEqual(path, [])

    def test_start_next_to_exit(self):
        grid = make_grid(["SE"])
        found, path, log = solve_maze(grid)
        self.assertTrue(found)
        self.assertEqual(path, [(0, 0), (0, 1)])

    def test_big_loop_does_not_hang(self):
        # lots of open space with loops, visited list should stop infinite loops
        grid = make_grid([
            "S....",
            ".....",
            ".....",
            "....E",
        ])
        found, path, log = solve_maze(grid)
        self.assertTrue(found)
        self.check_path(grid, path)

    def test_bad_mazes_raise(self):
        self.assertRaises(ValueError, make_grid, ["S..#E"])    # bad char
        self.assertRaises(ValueError, make_grid, ["....E"])    # no start
        self.assertRaises(ValueError, make_grid, ["S...."])    # no exit
        self.assertRaises(ValueError, make_grid, ["SS..E"])    # two starts
        self.assertRaises(ValueError, make_grid, ["", "  "])   # empty

    def test_load_from_file(self):
        # write a little maze to a temp file and load it back
        fd, filename = tempfile.mkstemp(suffix=".txt")
        f = os.fdopen(fd, "w")
        f.write("|||||\n|S.E|\n|||||\n")
        f.close()
        try:
            grid = load_maze_from_file(filename)
            found, path, log = solve_maze(grid)
            self.assertTrue(found)
            self.assertEqual(len(path), 3)
        finally:
            os.remove(filename)

    def test_maze_to_string_marks_path(self):
        grid = make_grid(["S.E"])
        found, path, log = solve_maze(grid)
        self.assertEqual(maze_to_string(grid, path), "S*E\n")


def run_tests():
    """runs every test above and prints how many passed."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestStack))
    suite.addTests(loader.loadTestsFromTestCase(TestParChecker))
    suite.addTests(loader.loadTestsFromTestCase(TestTokenize))
    suite.addTests(loader.loadTestsFromTestCase(TestInfixToPrefix))
    suite.addTests(loader.loadTestsFromTestCase(TestMaze))

    result = unittest.TextTestRunner(verbosity=2).run(suite)

    total = result.testsRun
    failed = len(result.failures) + len(result.errors)
    passed = total - failed
    if total > 0:
        rate = passed / total * 100
    else:
        rate = 0
    print("\npassed " + str(passed) + " / " + str(total) + " tests (" + str(round(rate, 1)) + "%)")


# ---------------------------------------------------------------
# menu stuff
# ---------------------------------------------------------------

def check_parens_menu():
    expr = input("enter an expression: ")
    if parChecker(expr):
        print("balanced :)")
    else:
        print("NOT balanced :(")


def convert_menu():
    expr = input("enter an infix expression (ex: (A + B) * C): ")
    show = input("show the step by step trace? (y/n): ").strip().lower()
    try:
        if show == "y":
            print()
            answer = infix_to_prefix(expr, True)
            print()
        else:
            answer = infix_to_prefix(expr)
        print("prefix: " + answer)
    except ValueError as e:
        print("couldn't convert it: " + str(e))


def run_maze(grid):
    """solves the grid and prints everything out."""
    print("\nthe maze:")
    print(maze_to_string(grid))

    found, path, log = solve_maze(grid)

    show = input("show the full traversal log? (y/n): ").strip().lower()
    if show == "y":
        print("\n--- traversal log ---")
        for line in log:
            print(line)
        print("---------------------")

    if found:
        print("\nfound a path! (" + str(len(path)) + " steps, '*' is the path)")
        print(maze_to_string(grid, path))
        print("path: " + " -> ".join(str(p) for p in path))
    else:
        print("\nno way out of this maze")


def sample_maze_menu():
    grid = make_grid(SAMPLE_MAZE)
    run_maze(grid)


def file_maze_menu():
    filename = input("enter the maze file name: ").strip()
    try:
        grid = load_maze_from_file(filename)
    except FileNotFoundError:
        print("couldn't find that file")
        return
    except ValueError as e:
        print("bad maze: " + str(e))
        return
    except OSError as e:
        print("couldn't read the file: " + str(e))
        return
    run_maze(grid)


def typed_maze_menu():
    print("type the maze one row at a time. use | . S E")
    print("press enter on an empty line when you're done")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    try:
        grid = make_grid(lines)
    except ValueError as e:
        print("bad maze: " + str(e))
        return
    run_maze(grid)


def print_menu():
    print("\n========= stack project =========")
    print("1. check if parentheses are balanced")
    print("2. convert infix to prefix (Polish)")
    print("3. solve the sample maze")
    print("4. load a maze from a file")
    print("5. type in a maze")
    print("6. run the test suite")
    print("0. quit")


def main():
    while True:
        print_menu()
        choice = input("pick an option: ").strip()

        if choice == "1":
            check_parens_menu()
        elif choice == "2":
            convert_menu()
        elif choice == "3":
            sample_maze_menu()
        elif choice == "4":
            file_maze_menu()
        elif choice == "5":
            typed_maze_menu()
        elif choice == "6":
            run_tests()
        elif choice == "0":
            print("bye!")
            break
        else:
            print("that's not an option, try again")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # so ctrl+c doesn't dump a big error
        print("\nbye!")
