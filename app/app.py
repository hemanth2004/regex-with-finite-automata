from app.regex.lexer import Lexer
from app.regex.parser import Parser
from app.ds.ast import ASTNode
from app.fa.fa import FA
from app.fa.fa_builder import FABuilder
from app.fa.nfa_to_dfa import convert_to_dfa
from app.fa.shortest_path import find_shortest_accepting_string
from app.fa.dfa_minimization import minimize_dfa

def build_fa(regex,
         verbose=False,
         if_remove_duplicate_transitions=False,
         if_convert_to_dfa=False,
         if_find_shortest_accepting_string=False,
         if_minimize_dfa=False, 
         if_report_stats=False):
    
    if verbose:
        print("regex:",regex)
    
    
    if if_report_stats:
        import time
        stats = {}
        start_time = time.time()
        
        # Tokenization stats
        token_start = time.time()
        lexer = Lexer(regex)
        tokens = lexer.tokenize()
        stats['tokenization_time'] = time.time() - token_start
        
        # Parsing stats
        parse_start = time.time()
        parser = Parser(tokens)
        ast = parser.parse()
        stats['parsing_time'] = time.time() - parse_start
        
        # FA Building stats
        fa_build_start = time.time()
        ast_list = []
        def add_to_list(node):
            ast_list.append(node)
        ast.traverse_postorder(add_to_list)
        fab = FABuilder()
        fa = fab.build_from_postorder(ast_list)
        stats['fa_building_time'] = time.time() - fa_build_start
        stats['initial_states'] = len(fa.states)
        stats['initial_transitions'] = fa.transitions.get_edges_count()
    else:
        lexer = Lexer(regex)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        ast_list = []
        def add_to_list(node):
            ast_list.append(node)
        ast.traverse_postorder(add_to_list)
        fab = FABuilder()
        fa = fab.build_from_postorder(ast_list)

    if verbose:
        print("\n=== Initial Finite Automaton ===")
        fa.pretty_print()

    if if_remove_duplicate_transitions:
        fa.remove_duplicate_transitions()

    if if_convert_to_dfa:
        if if_report_stats:
            dfa_start = time.time()
        fa = convert_to_dfa(fa)
        if if_report_stats:
            stats['dfa_conversion_time'] = time.time() - dfa_start
            stats['dfa_states'] = len(fa.states)
            stats['dfa_transitions'] = fa.transitions.get_edges_count()
    
    if if_minimize_dfa:
        if if_report_stats:
            min_start = time.time()
        fa = minimize_dfa(fa)
        if if_report_stats:
            stats['minimization_time'] = time.time() - min_start
            stats['minimized_states'] = len(fa.states)
            stats['minimized_transitions'] = fa.transitions.get_edges_count()

    if if_find_shortest_accepting_string:
        if if_report_stats:
            shortest_start = time.time()
        shortest_string, path = find_shortest_accepting_string(fa)
        if if_report_stats:
            stats['shortest_string_time'] = time.time() - shortest_start
        print(f"\n---\nShortest accepting string: {shortest_string}")
        print(f"Path: {path}")

    if if_report_stats:
        stats['total_time'] = time.time() - start_time
        print("\n=== Performance Statistics ===")
        print(f"Tokenization time: {stats['tokenization_time']:.7f} seconds")
        print(f"Parsing time: {stats['parsing_time']:.7f} seconds")
        print(f"FA building time: {stats['fa_building_time']:.7f} seconds")
        print(f"Initial FA states: {stats['initial_states']}")
        print(f"Initial FA transitions: {stats['initial_transitions']}")
        
        if if_convert_to_dfa:
            print(f"DFA conversion time: {stats['dfa_conversion_time']:.7f} seconds")
            print(f"DFA states: {stats['dfa_states']}")
            print(f"DFA transitions: {stats['dfa_transitions']}")
            
        if if_minimize_dfa:
            print(f"DFA minimization time: {stats['minimization_time']:.7f} seconds")
            print(f"Minimized DFA states: {stats['minimized_states']}")
            print(f"Minimized DFA transitions: {stats['minimized_transitions']}")
            if if_convert_to_dfa:
                state_reduction = ((stats['dfa_states'] - stats['minimized_states']) / stats['dfa_states']) * 100
                transition_reduction = ((stats['dfa_transitions'] - stats['minimized_transitions']) / stats['dfa_transitions']) * 100
                print(f"State reduction: {state_reduction:.1f}%")
                print(f"Transition reduction: {transition_reduction:.1f}%")
            
        if if_find_shortest_accepting_string:
            print(f"Shortest string finding time: {stats['shortest_string_time']:.7f} seconds")
            
        print(f"Total time: {stats['total_time']:.7f} seconds")

    return fa