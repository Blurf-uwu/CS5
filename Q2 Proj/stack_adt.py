# stack_adt.py
# module 1 - the Stack ADT that everything else in the project uses
# (built off the Stack class from my MP4, with error handling added)


class Stack:
    """
    a Stack, an abstract data type (ADT) that follows LIFO (last in, first out).

    think of it like a shuttlecock tube (the badminton kind). you can only
    put a shuttlecock in through the open top, and you can only take one out
    from the top too. the one you put in last is the first one you get back,
    and you can't reach the ones at the bottom without taking the top ones
    out first.

    that's how this class works. you only ever touch the top:
        push(item) - drop a shuttlecock in the top of the tube
        pop()      - take the top shuttlecock out
        peek()     - look at the top shuttlecock without taking it out
        isEmpty()  - check if the tube has nothing in it
        size()     - count how many shuttlecocks are in the tube
    """

    def __init__(self):
        """makes a new empty stack (an empty tube)."""
        # the list is only supposed to be used inside this class.
        # the end of the list is the top of the tube
        self.items = []

    def isEmpty(self):
        """returns True if the stack has no items, False otherwise."""
        return len(self.items) == 0

    def push(self, item):
        """puts item on the top of the stack."""
        self.items.append(item)

    def pop(self):
        """
        takes the top item off the stack and returns it.
        raises IndexError if the stack is empty (can't take a shuttlecock
        out of an empty tube).
        """
        if not self.isEmpty():
            return self.items.pop()
        # used to return None here but that hides bugs, so now it errors
        raise IndexError("pop from empty stack - there's nothing in the tube")

    def peek(self):
        """
        returns the top item but leaves it on the stack.
        raises IndexError if the stack is empty.
        """
        if not self.isEmpty():
            return self.items[-1]
        raise IndexError("peek at empty stack - there's nothing in the tube")

    def size(self):
        """returns how many items are in the stack."""
        return len(self.items)

    def __str__(self):
        # just for printing/debugging. shows the items bottom -> top with
        # spaces in between, so other files never have to touch self.items
        text = ""
        for item in self.items:
            text = text + str(item) + " "
        return text.strip()
