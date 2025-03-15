def generate_mermaid(fa):
    """
    Generates a Mermaid diagram text representation of a Finite Automaton.
    
    Args:
        fa: The Finite Automaton object
        
    Returns:
        str: Mermaid diagram text
    """
    result = ["stateDiagram-v2"]
    
    # Add states
    for state in fa.states:
        # Mark final states with double circles
        if state in fa.final_states:
            result.append(f"    {state}: {state}")
            result.append(f"    style {state} fill:#f9f,stroke-width:4px")
        
    # Add transitions
    for state in fa.states:
        state_index = list(fa.states).index(state)
        edges = fa.transitions.get_edges(state_index)
        
        for dest_index, symbol in edges:
            dest_state = list(fa.states)[dest_index]
            # Use ε for epsilon transitions
            label = "ε" if symbol == "" else symbol
            result.append(f"    {state} --> {dest_state}: {label}")
    
    # Mark starting state with an arrow
    if fa.starting_state:
        result.append(f"    [*] --> {fa.starting_state}")
    
    return "\n".join(result) 