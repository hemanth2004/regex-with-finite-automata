import numpy as np
from app.ds.set import Set
from app.ds.graph import Graph
from collections import deque

class FA:
    
    def __init__(self):
        self.states = Set()
        self._state_list = []  # Maintain ordered list of states
        self.final_states = Set()
        self.transitions = Graph(0)
        self.starting_state = None

    def epsilon_closure(self, states):
        """
        Compute the epsilon closure of a set of states.
        That is, all states reachable from these states via epsilon (empty string) transitions.
        """
        closure = Set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            state_index = list(self.states).index(state)
            edges = self.transitions.get_edges(state_index)
            
            for dest_index, symbol in edges:
                if symbol == "":  # epsilon transition
                    dest_state = list(self.states)[dest_index]
                    if dest_state not in closure:
                        closure.add(dest_state)
                        stack.append(dest_state)

        return closure

    def run(self, input_string):
        """
        Simulates the epsilon-NFA on an input string.
        Each execution thread maintains its own remaining input.
        Uses visited set to prevent infinite loops through epsilon transitions.
        """
        from collections import deque

        # Start with epsilon closure of the starting state
        initial_states = self.epsilon_closure(Set([self.starting_state]))
        queue = deque([(state, input_string) for state in initial_states])
        
        # Keep track of visited (state, remaining_input) pairs
        visited = set()
        
        while queue:
            state, remaining_input = queue.popleft()
            
            if (state, remaining_input) in visited:
                continue
                
            visited.add((state, remaining_input))
            
            if not remaining_input and state in self.final_states:
                return True
                
            # Use consistent state indexing
            state_index = self.get_state_index(state)
            edges = self.transitions.get_edges(state_index)
            
            for dest_index, symbol in edges:
                # Use _state_list for consistent state lookup
                dest_state = self._state_list[dest_index]
                if symbol == "":
                    if (dest_state, remaining_input) not in visited:
                        queue.append((dest_state, remaining_input))
                elif remaining_input and remaining_input[0] == symbol:
                    new_input = remaining_input[1:]
                    if (dest_state, new_input) not in visited:
                        queue.append((dest_state, new_input))
        
        return False
    
    def remove_duplicate_transitions(self):
        """
        Minimizes the FA by removing duplicate transitions.
        """
        self.transitions.remove_duplicate_edges()

    def add_state(self, state):
        if state not in self.states:
            self.states.add(state)
            self._state_list.append(state)
            self.transitions.add_vertex()

    def get_state_index(self, state):
        """Get the consistent index for a state"""
        return self._state_list.index(state)

    def del_state(self, state):
        if state in self.states:
            state_index = list(self.states).index(state)
            self.states.remove(state)
            if state in self.final_states:
                self.final_states.remove(state)
            self.transitions.delete_vertex(state_index)

    def add_final_state(self, state):
        self.final_states.add(state)

    def del_final_state(self, state):
        self.final_states.remove(state)

    def add_transition(self, state_from, input_string, state_to):
        """
        Adds a transition for a given input string.
        The input can be an epsilon transition ("" for empty string).
        """
        from_index = list(self.states).index(state_from)
        to_index = list(self.states).index(state_to)
        self.transitions.add_edge(from_index, to_index, input_string)

    def del_transition(self, state_from, input_string, state_to):
        from_index = list(self.states).index(state_from)
        to_index = list(self.states).index(state_to)
        self.transitions.delete_edge(from_index, to_index, input_string)

    def get_alphabet(self):
        """
        Returns the alphabet of the FA.
        """
        alphabet = Set()
        for state in self.states:
            state_index = list(self.states).index(state)
            edges = self.transitions.get_edges(state_index)
            for _, input_string in edges:
                if input_string == "":
                    alphabet.add('')
                else:
                    for char in input_string:
                        alphabet.add(char)
        return alphabet

    def pretty_print(self):
        """
        Pretty prints the finite automaton.
        """
        print("Finite Automaton:")
        print("=================")
        print(f"States ({len(self.states)}): {', '.join(map(str, self.states))}")
        print(f"Starting State: {self.starting_state}")
        print(f"Final States ({len(self.final_states)}): {', '.join(map(str, self.final_states))}")
        print(f"Transitions ({self.transitions.get_edges_count()}):")
        
        # Get all transitions for each state
        for state in self.states:
            state_index = list(self.states).index(state)
            edges = self.transitions.get_edges(state_index)
            if edges:  # If state has outgoing transitions
                for dest_index, input_string in edges:
                    dest_state = list(self.states)[dest_index]
                    print(f"  {state} --[{input_string}]--> {dest_state}")
            else:  # If state has no outgoing transitions
                print(f"  {state} (no outgoing transitions)")
        
        print(f"Alphabet: {', '.join(map(str, self.get_alphabet()))}")

    

