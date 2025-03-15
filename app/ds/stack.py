class Stack:
    def __init__(self):
        """Initialize an empty stack."""
        self._items = []

    def push(self, item):
        """Push an item onto the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item of the stack. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item of the stack without removing it. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("Peek from an empty stack")
        return self._items[-1]

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self._items)

    def __repr__(self):
        """Return a string representation of the stack."""
        return f"Stack({self._items})"
