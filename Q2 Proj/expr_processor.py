# expr_processor.py
# module 2 - checks parentheses and turns infix math into Polish (prefix) notation

from stack_adt import Stack

# how strong each operator is. bigger number = do it first
PRECEDENCE = {
    "^": 3,
    "*": 2,
    "/": 2,
    "+": 1,
    "-": 1,
}


def parChecker(expr):
    """
    checks if the parentheses in expr are balanced.
    every '(' gets pushed, every ')' pops one off. if we try to pop when the
    stack is already empty that means there's an extra ')' so we fail early.
    returns True if balanced, False if not.
    """
    s = Stack()

    for ch in expr:
        if ch == "(":
            s.push(ch)
        elif ch == ")":
            # early failure - a ')' showed up with no '(' to match it
            if s.isEmpty():
                return False
            s.pop()

    # if anything is left over then some '(' never got closed
    return s.isEmpty()


def tokenize(expr):
    """
    splits an expression string into a list of tokens.
    numbers like 12 or 3.5 and names like abc stay together as one token.
    spaces get skipped. raises ValueError if there's a weird character.
    """
    tokens = []
    current = ""  # used to build up numbers / variable names

    for ch in expr:
        if ch.isalnum() or ch == "." or ch == "_":
            current = current + ch
        else:
            # we hit something that isn't part of a number/name so save what we have
            if current != "":
                tokens.append(current)
                current = ""

            if ch == " " or ch == "\t":
                continue
            elif ch in PRECEDENCE or ch == "(" or ch == ")":
                tokens.append(ch)
            else:
                raise ValueError("invalid character in expression: '" + ch + "'")

    # don't forget the last number/name
    if current != "":
        tokens.append(current)

    return tokens


def is_operand(token):
    """returns True if the token is a number or variable (not an operator or paren)."""
    return token not in PRECEDENCE and token != "(" and token != ")"


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
            elif is_operand(t):
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
    notation (like "* + A B C").

    how it works:
      1. tokenize the expression and reverse the tokens
      2. scan the reversed tokens (so really we're going right to left)
      3. since everything is backwards, ')' acts like an opening bracket and
         '(' acts like a closing bracket
      4. operators go on a stack, higher precedence ones get popped to output
      5. reverse the output at the end to get the prefix answer

    if show_steps is True it prints a little trace table of each step.
    returns the prefix expression as a string with spaces between tokens.
    raises ValueError if the expression is invalid.
    """
    if not parChecker(expr):
        raise ValueError("parentheses are not balanced")

    tokens = tokenize(expr)
    check_infix(tokens)

    # step 1 - reverse the tokens
    reversed_tokens = []
    i = len(tokens) - 1
    while i >= 0:
        reversed_tokens.append(tokens[i])
        i = i - 1

    op_stack = Stack()
    output = []

    if show_steps:
        print("{:<8}{:<25}{}".format("token", "stack (bottom->top)", "output"))
        print("-" * 55)

    # step 2 - scan through (right to left on the original)
    for token in reversed_tokens:
        if is_operand(token):
            output.append(token)

        elif token == ")":
            # backwards, so ')' is the opening one
            op_stack.push(token)

        elif token == "(":
            # backwards, so '(' is the closing one. pop until we find the ')'
            while op_stack.peek() != ")":
                output.append(op_stack.pop())
            op_stack.pop()  # throw away the ')'

        else:
            # it's an operator
            while not op_stack.isEmpty() and op_stack.peek() != ")":
                top = op_stack.peek()
                # pop operators that are higher precedence than this one.
                # ^ is right associative so for ^ we also pop equal ones
                # (that's what makes a^b^c come out as ^ a ^ b c)
                if PRECEDENCE[top] > PRECEDENCE[token]:
                    output.append(op_stack.pop())
                elif token == "^" and top == "^":
                    output.append(op_stack.pop())
                else:
                    break
            op_stack.push(token)

        if show_steps:
            print("{:<8}{:<25}{}".format(token, str(op_stack), " ".join(output)))

    # whatever operators are left go to the output
    while not op_stack.isEmpty():
        output.append(op_stack.pop())

    if show_steps:
        print("{:<8}{:<25}{}".format("(end)", "", " ".join(output)))

    # step 5 - reverse the output to get the prefix expression
    prefix = []
    i = len(output) - 1
    while i >= 0:
        prefix.append(output[i])
        i = i - 1

    return " ".join(prefix)
