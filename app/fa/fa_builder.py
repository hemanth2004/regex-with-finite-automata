from app.ds.ast import ASTNode
from app.ds.stack import Stack
from app.fa.fa import FA


class FABuilder:
    def __init__(self):
        self.state_counter = 0

    def new_state(self):
        """Returns a unique state ID"""
        self.state_counter += 1
        return f"q{self.state_counter}"

    def build_from_postorder(self, postorder_list):
        """Build FA from a postorder-traversed AST"""
        stack = []
        fa = FA()

        def create_basic_fa(char):
            """Creates a basic FA for a single character"""
            start = self.new_state()
            end = self.new_state()
            fa.add_state(start)
            fa.add_state(end)
            fa.add_transition(start, char, end)
            return (start, end)

        def concat_fa(fa1, fa2):
            """Concatenates two FAs"""
            # Connect fa1's end to fa2's start with epsilon transition
            fa.add_transition(fa1[1], "", fa2[0])
            return (fa1[0], fa2[1])

        def union_fa(fa1, fa2):
            """Creates a union (|) of two FAs"""
            start = self.new_state()
            end = self.new_state()
            fa.add_state(start)
            fa.add_state(end)
            
            # Connect new start to both FA starts
            fa.add_transition(start, "", fa1[0])
            fa.add_transition(start, "", fa2[0])
            
            # Connect both FA ends to new end
            fa.add_transition(fa1[1], "", end)
            fa.add_transition(fa2[1], "", end)
            
            return (start, end)

        def star_fa(fa1):
            """Creates a Kleene star (*) of an FA"""
            start = self.new_state()
            end = self.new_state()
            fa.add_state(start)
            fa.add_state(end)
            
            # Empty string case
            fa.add_transition(start, "", end)
            
            # Normal case
            fa.add_transition(start, "", fa1[0])
            fa.add_transition(fa1[1], "", end)
            
            # Repeat case
            fa.add_transition(fa1[1], "", fa1[0])
            
            return (start, end)

        # Process each node in postorder
        for node in postorder_list:
            if node.type == "SYMBOL":
                stack.append(create_basic_fa(node.value))
            elif node.type == "CONCAT":
                fa2 = stack.pop()
                fa1 = stack.pop()
                stack.append(concat_fa(fa1, fa2))
            elif node.type == "UNION":
                fa2 = stack.pop()
                fa1 = stack.pop()
                stack.append(union_fa(fa1, fa2))
            elif node.type == "STAR":
                fa1 = stack.pop()
                stack.append(star_fa(fa1))

        # Set the final states and starting state
        if stack:
            start, end = stack.pop()
            fa.starting_state = start
            fa.add_final_state(end)
            
            # Make sure all states are added to the FA
            fa.add_state(start)
            fa.add_state(end)

        return fa
