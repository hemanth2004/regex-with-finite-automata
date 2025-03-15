from app.ds.dsu import DSU
from app.fa.fa import FA
from app.ds.set import Set

def minimize_dfa(fa):
    """
    Minimizes a DFA using Hopcroft's algorithm with Union-Find data structure.
    Returns a new minimized FA.
    """
    # Initialize new FA
    minimized_fa = FA()
    
    # Convert states to indices for DSU
    state_to_idx = {state: idx for idx, state in enumerate(fa.states)}
    idx_to_state = {idx: state for state, idx in state_to_idx.items()}
    
    # Initialize DSU with two initial partitions: final and non-final states
    dsu = DSU(len(fa.states))
    
    # Initially merge all final states
    final_states_list = list(fa.final_states)
    for i in range(len(final_states_list) - 1):
        dsu.union(
            state_to_idx[final_states_list[i]],
            state_to_idx[final_states_list[i + 1]]
        )
    
    # Initially merge all non-final states
    non_final_states = fa.states.difference(fa.final_states)
    non_final_states_list = list(non_final_states)
    for i in range(len(non_final_states_list) - 1):
        dsu.union(
            state_to_idx[non_final_states_list[i]],
            state_to_idx[non_final_states_list[i + 1]]
        )
    
    # Refine partitions based on transitions
    changed = True
    alphabet = fa.get_alphabet()
    
    while changed:
        changed = False
        current_sets = dsu.get_sets()
        
        for symbol in alphabet:
            if symbol == '':  # Skip epsilon transitions for DFA
                continue
                
            for partition in current_sets:
                partition_list = list(partition)
                if len(partition_list) <= 1:
                    continue
                    
                # Get transition destinations for first state
                first_state = idx_to_state[partition_list[0]]
                first_state_idx = state_to_idx[first_state]
                first_transitions = fa.transitions.get_edges(first_state_idx)
                first_dest = None
                
                for dest_idx, sym in first_transitions:
                    if sym == symbol:
                        first_dest = dsu.find(dest_idx)
                        break
                
                # Compare with other states in partition
                split_needed = False
                states_to_split = []
                
                for state_idx in partition_list[1:]:
                    state = idx_to_state[state_idx]
                    transitions = fa.transitions.get_edges(state_to_idx[state])
                    current_dest = None
                    
                    for dest_idx, sym in transitions:
                        if sym == symbol:
                            current_dest = dsu.find(dest_idx)
                            break
                    
                    # If destinations are in different partitions, mark for splitting
                    if first_dest != current_dest:
                        split_needed = True
                        states_to_split.append(state_idx)
                
                # If split is needed, perform it
                if split_needed:
                    changed = True
                    # Split states into new partition
                    for state_idx in states_to_split:
                        dsu.split(state_idx)
                    break
                    
            if changed:
                break
    
    # Create new minimized DFA
    final_partitions = dsu.get_sets()
    
    # Create new states for each partition
    partition_to_new_state = {}
    for partition in final_partitions:
        new_state = f"q{len(partition_to_new_state)}"
        partition_to_new_state[frozenset(partition)] = new_state
        minimized_fa.add_state(new_state)
        
        # Check if partition contains any final states
        for state_idx in partition:
            if idx_to_state[state_idx] in fa.final_states:
                minimized_fa.add_final_state(new_state)
                break
        
        # Set starting state
        if any(idx_to_state[state_idx] == fa.starting_state for state_idx in partition):
            minimized_fa.starting_state = new_state
    
    # Add transitions
    for partition in final_partitions:
        # Take first state from partition as representative
        rep_state_idx = list(partition)[0]
        rep_state = idx_to_state[rep_state_idx]
        from_state = partition_to_new_state[frozenset(partition)]
        
        # Get transitions
        transitions = fa.transitions.get_edges(state_to_idx[rep_state])
        for dest_idx, symbol in transitions:
            if symbol == '':  # Skip epsilon transitions
                continue
            
            # Find which partition contains the destination state
            dest_partition = next(
                p for p in final_partitions 
                if dsu.find(dest_idx) in p
            )
            to_state = partition_to_new_state[frozenset(dest_partition)]
            
            # Add transition to minimized DFA
            minimized_fa.add_transition(from_state, symbol, to_state)
    
    return minimized_fa

