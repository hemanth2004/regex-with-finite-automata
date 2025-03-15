from collections import defaultdict
import heapq
from app.ds.set import Set

def find_shortest_accepting_string(fa):
    """
    Finds the shortest string that would be accepted by the FA.
    Uses a modified Dijkstra's algorithm to find shortest path to any final state.
    
    Args:
        fa: The finite automaton
        
    Returns:
        tuple: (shortest_string, path_of_states) or (None, None) if no accepting string exists
    """
    # Priority queue entries are (path_length, current_state, path_string, path_states)
    pq = [(0, fa.starting_state, "", [fa.starting_state])]
    visited = Set()
    
    while pq:
        length, current, string, path = heapq.heappop(pq)
        
        # If we've reached a final state, we've found the shortest path
        if current in fa.final_states:
            return string, path
            
        # Skip if we've seen this state
        if current in visited:
            continue
            
        visited.add(current)
        
        # Get all transitions from current state
        current_index = list(fa.states).index(current)
        edges = fa.transitions.get_edges(current_index)
        
        # Add all possible next states to priority queue
        for dest_index, symbol in edges:
            dest_state = list(fa.states)[dest_index]
            if dest_state not in visited:
                # For epsilon transitions, don't increase path length
                new_length = length if symbol == "" else length + 1
                new_string = string if symbol == "" else string + symbol
                new_path = path + [dest_state]
                heapq.heappush(pq, (new_length, dest_state, new_string, new_path))
    
    # No accepting string found
    return None, None

def find_all_shortest_accepting_strings(fa, max_count=5):
    """
    Finds multiple shortest strings that would be accepted by the FA.
    Returns up to max_count different strings of the same minimum length.
    
    Args:
        fa: The finite automaton
        max_count: Maximum number of strings to return
        
    Returns:
        list of tuples: [(string, path), ...] sorted by string
    """
    # Priority queue entries are (path_length, current_state, path_string, path_states)
    pq = [(0, fa.starting_state, "", [fa.starting_state])]
    visited = defaultdict(Set)  # state -> Set of strings seen at this state
    results = []
    min_length = None
    
    while pq and (min_length is None or len(results) < max_count):
        length, current, string, path = heapq.heappop(pq)
        
        # If we've found a longer path than our shortest solution, we can stop
        if min_length is not None and length > min_length:
            break
            
        # If we've reached a final state
        if current in fa.final_states:
            if min_length is None:
                min_length = length
            if length == min_length:
                results.append((string, path))
            continue
            
        # Skip if we've seen this state with this string length
        if length in visited[current]:
            continue
            
        visited[current].add(length)
        
        # Get all transitions from current state
        current_index = list(fa.states).index(current)
        edges = fa.transitions.get_edges(current_index)
        
        # Add all possible next states to priority queue
        for dest_index, symbol in edges:
            dest_state = list(fa.states)[dest_index]
            # For epsilon transitions, don't increase path length
            new_length = length if symbol == "" else length + 1
            new_string = string if symbol == "" else string + symbol
            new_path = path + [dest_state]
            heapq.heappush(pq, (new_length, dest_state, new_string, new_path))
    
    # Sort results by string for deterministic output
    return sorted(results) 