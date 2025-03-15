from app.ds.set import Set
from app.fa.fa import FA
from collections import deque

def convert_to_dfa(nfa):
    """
    Converts NFA to DFA using BFS to explore state combinations.
    
    Args:
        nfa: The input NFA (FA object)
    
    Returns:
        A new FA object that is deterministic
    """
    dfa = FA()
    
    # Get alphabet (excluding epsilon)
    alphabet = Set()
    for state in nfa.states:
        state_index = list(nfa.states).index(state)
        edges = nfa.transitions.get_edges(state_index)
        for _, symbol in edges:
            if symbol != "":
                alphabet.add(symbol)
    
    # Start with epsilon closure of initial state
    initial_states = nfa.epsilon_closure(Set([nfa.starting_state]))
    
    # BFS queue and visited set
    queue = deque([initial_states])
    visited = Set()  # Set of frozensets
    
    # Map NFA state combinations to DFA state names
    state_counter = 0
    state_map = {}
    
    while queue:
        current_states = queue.popleft()
        current_key = current_states.to_frozenset()
        
        # Skip if we've seen this combination
        if current_key in visited:
            continue
            
        # Mark as visited
        visited.add(current_key)
        
        # Create new DFA state for this combination
        if current_key not in state_map:
            dfa_state = f"q{state_counter}"
            state_map[current_key] = dfa_state
            state_counter += 1
            
            # Add state to DFA
            dfa.add_state(dfa_state)
            
            # Mark as final if it contains any final states
            if any(state in nfa.final_states for state in current_states):
                dfa.add_final_state(dfa_state)
        
        current_dfa_state = state_map[current_key]
        
        # For each input symbol
        for symbol in alphabet:
            next_states = Set()
            
            # Get all possible next states
            for state in current_states:
                state_index = list(nfa.states).index(state)
                edges = nfa.transitions.get_edges(state_index)
                
                for dest_index, edge_symbol in edges:
                    if edge_symbol == symbol:
                        dest_state = list(nfa.states)[dest_index]
                        # Include epsilon closure of destination
                        next_states.update(nfa.epsilon_closure(Set([dest_state])))
            
            # If we have next states
            if next_states:
                next_key = next_states.to_frozenset()
                
                # Create new DFA state if needed
                if next_key not in state_map:
                    dfa_state = f"q{state_counter}"
                    state_map[next_key] = dfa_state
                    state_counter += 1
                    dfa.add_state(dfa_state)
                    
                    # Mark as final if needed
                    if any(state in nfa.final_states for state in next_states):
                        dfa.add_final_state(dfa_state)
                    
                    # Add to BFS queue
                    queue.append(next_states)
                
                # Add transition
                dfa.add_transition(current_dfa_state, symbol, state_map[next_key])
    
    # Set initial state
    dfa.starting_state = state_map[initial_states.to_frozenset()]
    
    return dfa
