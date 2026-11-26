# expr_processor.py
# module 2 - checks parentheses and turns infix math into Polish (prefix) notation
# (parChecker, tokenize and infix_to_prefix are from my MP4, cleaned up a bit)

from stack_adt import Stack

# how strong each operator is. bigger number = do it first
PRECEDENCE = {"^": 3, "*": 2, "/": 2, "+": 1, "-": 1}


def parChecker(symbol_string):
    """
    check if the parentheses in a string are balanced.

    the string is read from left to right. every '(' is pushed onto a stack,
    and every ')' pops one '(' off the stack. if we try to pop when the stack
    is already empty, there are too many ')' so it fails early.
    returns True if balanced, False if not.
    """
    s = Stack()

    for symbol in symbol_string:
        if symbol == "(":
            s.push(symbol)
        elif symbol == ")":
            # a ')' with nothing to match means it's unbalanced, stop right here
            if s.isEmpty():
                return False
            s.pop()

    # balanced only if every '(' was matched
    return s.isEmpty()


def tokenize(expr):
    """
    split an expression into a list of tokens.

    letters and digits that are next to each other are grouped into one
    operand, so "AB + 10" becomes ['AB', '+', '10'] instead of
    ['A', 'B', '+', '1', '0']. operators and parentheses are their own
    tokens, and spaces are skipped. raises ValueError on weird characters.
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
            if ch == " " or ch == "\t":
                continue
            elif ch in PRECEDENCE or ch == "(" or ch == ")":
                tokens.append(ch)
            else:
                raise ValueError("invalid character in expression: '" + ch + "'")

    # save the last operand if the expression ends with one
    if current != "":
        tokens.append(current)

    return tokens


def check_infix(tokens):
    """
    makes sure the tokens are in a valid infix order, like
    operand operator operand ... and parens in the right spots.
    raises ValueError with a message if something is off.
    """
    if len(tokens) == 0:
        raise ValueError("expression is empty")

    expect_operand = True  # at the start we need a number or a '('

    for t in tokens:
        if expect_operand:
            if t == "(":
                continue  # still waiting for an operand after a '('
            elif t.isalnum():
                expect_operand = False
            else:
                raise ValueError("expected a number or variable but got '" + t + "'")
        else:
            if t == ")":
                continue  # still waiting for an operator after a ')'
            elif t in PRECEDENCE:
                expect_operand = True
            else:
                raise ValueError("expected an operator but got '" + t + "'")

    if expect_operand:
        raise ValueError("expression can't end with an operator")


def infix_to_prefix(expr, show_steps=False):
    """
    converts an infix expression (like "(A + B) * C") into prefix / Polish
    notation (like "* + A B C") using a right-to-left scan.

    how it works:
      1. tokenize, push ')' on the stack and stick a '(' at the start of the
         tokens so it's the last thing read when going backwards
      2. scan the tokens in reverse (right to left). since we're going
         backwards, ')' acts like the opening bracket and '(' like the closing one
      3. operands go straight to the output, operators go on the stack and
         higher precedence ones get popped to the output
      4. reverse the output at the end to get the prefix answer

    if show_steps is True it prints a little trace table of each step.
    raises ValueError if the expression is invalid.
    """
    if not parChecker(expr):
        raise ValueError("parentheses are not balanced")

    tokens = tokenize(expr)
    check_infix(tokens)

    stack = Stack()
    out = []

    # step 1: push ')' to stack and add '(' to the start of the expression
    tokens = ["("] + tokens
    stack.push(")")

    if show_steps:
        print("{:<8}{:<25}{}".format("token", "stack (bottom->top)", "output"))
        print("-" * 55)

    # step 2: scan right-to-left
    for ch in reversed(tokens):
        if ch.isalnum():
            out.append(ch)
        elif ch == ")":
            stack.push(ch)
        elif ch in PRECEDENCE:
            # pop operators that are higher precedence than this one.
            # ^ goes right to left (a^b^c = a^(b^c)) so for ^ we also pop
            # another ^ that's sitting on top, otherwise it comes out wrong
            while (
                not stack.isEmpty()
                and stack.peek() != ")"
                and stack.peek() in PRECEDENCE
                and (PRECEDENCE[stack.peek()] > PRECEDENCE[ch]
                     or (ch == "^" and stack.peek() == "^"))
            ):
                out.append(stack.pop())
            stack.push(ch)
        elif ch == "(":
            # pop everything until the matching ')'
            while not stack.isEmpty() and stack.peek() != ")":
                out.append(stack.pop())
            if not stack.isEmpty() and stack.peek() == ")":
                stack.pop()

        if show_steps:
            print("{:<8}{:<25}{}".format(ch, str(stack), " ".join(out)))

    # flush any remaining operators
    while not stack.isEmpty():
        top = stack.pop()
        if top not in ("(", ")"):
            out.append(top)

    # step 3: reverse the output to get prefix
    return " ".join(out[::-1])
