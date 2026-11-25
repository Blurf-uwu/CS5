"""
Building the Stack ADT & Implementing Polish Notation Conversion in Python.

contains:
    1. parChecker      - checks if a string of parentheses is balanced.
    2. infix_to_prefix - converts an infix expression to prefix (Polish) notation
                         using a right-to-left scan.
"""

class Stack:
    """
    A Stack, an abstract data type (ADT)
    """
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.isEmpty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.isEmpty():
            return self.items[-1]
        return None

    def size(self):
        return len(self.items)


def parChecker(symbol_string):
    """
    Check if the parentheses in a string are balanced.

    The string is read from left to right. Every '(' is pushed onto a stack,
    and every ')' pops one '(' off the stack. If we try to pop when the stack
    is already empty, there are too many ')' so the string is not balanced.
    """
    s = Stack()

    for symbol in symbol_string:
        if symbol == "(":
            s.push(symbol)
        elif symbol == ")":
            # A ')' with nothing to match means it is unbalanced.
            if s.isEmpty():
                return False
            s.pop()

    # Balanced only if every '(' was matched.
    return s.isEmpty()


def tokenize(expr):
    """
    Split an expression into a list of tokens.

    Letters and digits that are next to each other are grouped into one
    operand, so "AB + 10" becomes ['AB', '+', '10'] instead of
    ['A', 'B', '+', '1', '0']. Operators and parentheses are their own
    tokens, and spaces are skipped.
    """
    tokens = []
    current = ""

    for ch in expr:
        if ch.isalnum():
            # still building the same operand
            current = current + ch
        else:
            # operand finished, save it before handling this character
            if current != "":
                tokens.append(current)
                current = ""
            if ch != " ":
                tokens.append(ch)

    # save the last operand if the expression ends with one
    if current != "":
        tokens.append(current)

    return tokens

def infix_to_prefix(expr):
    prec = {"^": 3, "*": 2, "/": 2, "+": 1, "-": 1}
    stack = Stack()
    out = []

    # Step 1: tokenize, push ')' to stack and add '(' to the start of the
    # expression so it is the last token read when scanning backwards
    tokens = ["("] + tokenize(expr)
    stack.push(")")

    # Step 2: scan right-to-left
    for ch in reversed(tokens):
        if ch.isalnum(): 
            out.append(ch)
        elif ch == ")": 
            stack.push(ch)
        elif ch in prec: 
            while (
                not stack.isEmpty()
                and stack.peek() != ")"
                and stack.peek() in prec
                and prec[stack.peek()] > prec[ch]
            ):
                out.append(stack.pop())
            stack.push(ch)
        elif ch == "(": 
            while not stack.isEmpty() and stack.peek() != ")":
                out.append(stack.pop())
            if not stack.isEmpty() and stack.peek() == ")":
                stack.pop()

    # flush any remaining operators
    while not stack.isEmpty():
        top = stack.pop()
        if top not in ("(", ")"):
            out.append(top)

    return " ".join(out[::-1])

def run_tests():
    """
    Runs the test cases 
    """
    print("Test 1:", parChecker("((()))"))
    print("Test 2:", parChecker("(()()"))
    print("Test 3:", parChecker("())"))
    print("Test 4:", infix_to_prefix("A + B"))
    print("Test 5:", infix_to_prefix("(A + B) * (C - D)"))
    print("Test 6:", infix_to_prefix("A * (B - C)"))


if __name__ == "__main__":
    run_tests()