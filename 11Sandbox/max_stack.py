class MaxStack:
    """Explanation of Max Stack Implemented in O(1)
    The problem requires implementing a stack that supports three operations in constant time (O(1)):

    Push(x) – Add an element x to the stack.
    Pop() – Remove the top element from the stack.
    Max() – Retrieve the maximum element currently in the stack."""

    def __init__(self):
        self.stack = []  # Main stack to store elements
        self.max_stack = []  # Auxiliary stack to track max values

    def push(self, val: int):
        """Push a value onto the stack and update the max stack."""
        self.stack.append(val)
        if not self.max_stack or val >= self.max_stack[-1]:
            self.max_stack.append(val)

    def pop(self) -> int:
        """Remove and return the top element. Raises an exception if the stack is empty."""
        if not self.stack:
            raise IndexError("Pop operation failed: Stack is empty.")

        val = self.stack.pop()
        if val == self.max_stack[-1]:
            self.max_stack.pop()
        return val

    def max(self) -> int:
        """Return the maximum element in the stack. Raises an exception if the stack is empty."""
        if not self.max_stack:
            raise ValueError("Max operation failed: Stack is empty.")

        return self.max_stack[-1]


# Example usage with exception handling
try:
    ms = MaxStack()
    ms.push(1)
    ms.push(3)
    ms.push(2)

    print("Current max:", ms.max())  # Output: 3
    print("Popped:", ms.pop())  # Output: 2
    print("Current max:", ms.max())  # Output: 3
    print("Popped:", ms.pop())  # Output: 3
    print("Current max:", ms.max())  # Output: 1
    print("Popped:", ms.pop())  # Output: 1

    print("Trying to get max from empty stack:")
    print(ms.max())  # This will raise an exception

except Exception as e:
    print("Exception:", e)
