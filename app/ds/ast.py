class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children or []

    def __repr__(self):
        if self.value is not None:
            return f"ASTNode({self.type}, {self.value}, {self.children})"
        return f"ASTNode({self.type}, {self.children})"

    def traverse_postorder(self, func):
        for child in reversed(self.children):
            child.traverse_postorder(func)
        func(self)

    def pretty_print(self, depth=0, last=True, prefix=""):
        """
        Pretty prints this AST node and its children with ASCII art.
        
        Args:
            depth: Current indentation depth (default: 0)
            last: Whether this is the last child of its parent (default: True)
            prefix: The prefix string for the current line (default: "")
        """
        # Create the current line's prefix
        current_prefix = prefix + ("└── " if last else "├── ")
        
        # Print the current node
        print(f"{current_prefix}{self.type}", end="")
        if self.value is not None:
            print(f"({self.value})")
        else:
            print()
        
        # Create the prefix for children
        child_prefix = prefix + ("    " if last else "│   ")
        
        # Print children
        if self.children:
            for i, child in enumerate(self.children):
                is_last = (i == len(self.children) - 1)
                child.pretty_print(depth + 1, is_last, child_prefix)

        
