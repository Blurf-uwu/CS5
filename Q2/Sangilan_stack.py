"""
Parts A and B in pdf attached
"""

# Part C:

class Stack:
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


def infix_to_prefix(expr):
    prec = {"^": 3, "*": 2, "/": 2, "+": 1, "-": 1}
    stack = Stack()
    out = []

    # Step 1: push ')' to stack and append '(' to the end of the expression
    mod_expr = expr.replace(" ", "") + "("
    stack.push(")")

    # Step 2: scan right-to-left 
    for ch in reversed(mod_expr):
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


if __name__ == "__main__":
    infix = input("Enter infix expression: ").strip()
    if infix:
        print("Prefix: " + infix_to_prefix(infix))