with open('./test.stupidlang') as file:
    keywords = {'if', 'else', 'end', 'print', 'ask_int'}
    tokens = [] # list of tuples like (type, value)
    for line in file:
        words = line.rstrip("\n").split(" ")

        for word in words:
            if word == '':
                pass
            elif word.isdigit():
                tokens.append(('INT', int(word)))
            elif word[0] == "_":
                tokens.append(('STR', word[1:].replace('_', ' ')))
            elif word in keywords: 
                tokens.append(('KEYWORD', word))
            elif all(ch in "=<>-!" for ch in word):
                tokens.append(('OPERATOR', word))
            elif word.upper() != word.lower():
                tokens.append(('VAR', word))
            else:
                print(f"Invalid token: {word}")
                exit(1)
        tokens.append(('EOL', None))
    tokens.append(('EOF', None))

#print(tokens)

# Epic 
# brain fog clearing
# martial englightenment giving
# zhong tang clan poshion level
# sentence thingy
# "Statements are different from expressions"

# Parse functions

def parse_list_of_statements():
    statements = []
    while True:
        st = parse_statement()
        if not st:
            break
        statements.append(st)
    return statements

def parse_program():
    statements = parse_list_of_statements()
    assert tokens[0][0] == 'EOF'
    return ('program', statements)


def parse_statement():
    node = parse_print() or parse_assignment() or parse_if_else()
    if node:
        assert tokens.pop(0)[0] == 'EOL'
        return node

    return None

def parse_print():
    if tokens[0] != ('KEYWORD', 'print'):
        return None
    tokens.pop(0)
    expr = parse_expression()
    assert expr is not None
    return ('print', expr)

def parse_assignment():
    if tokens[0][0] == 'VAR' and tokens[1][1] == '<-':
        var = tokens.pop(0)
        tokens.pop(0)
        expr = parse_expression()
        assert expr is not None
        return ('assignment', var, expr)
    return None

def parse_ask_int():
    if tokens[0] != ('KEYWORD', 'ask_int'):
        return None
    tokens.pop(0)
    expr = parse_expression()
    assert expr is not None
    return ('ask_int', expr)
    pass

def parse_expression():
    if tokens[0][0] in {'STR', 'INT', 'VAR'}:
        return tokens.pop(0)
    return parse_ask_int()

def parse_if_else():
    if tokens[0] != ('KEYWORD', 'if'):
        return None
    
    tokens.pop(0)
    
    left = parse_expression()
    assert left is not None 

    operator = tokens.pop(0)
    assert operator[0] == 'OPERATOR'

    right = parse_expression()
    assert right is not None 

    assert tokens.pop(0)[0] == 'EOL'

    true_statements = parse_list_of_statements()

    false_statements = None
    if tokens[0] == ('KEYWORD', 'else'):
        tokens.pop(0)
        assert tokens.pop(0)[0] == 'EOL' 
        false_statements = parse_list_of_statements()

    assert tokens.pop(0) == ('KEYWORD', 'end')

    return ('if_else', left, operator, right, true_statements, false_statements)
 

def pretty_print_parse_tree(tree, indent=0):
    """
    Recursively prints the parse tree in a more readable format.

    Args:
        tree: The parse tree (nested tuples/lists).
        indent: The current indentation level.
    """
    if isinstance(tree, tuple):
        node_type = tree[0]
        node_values = tree[1:]

        print("  " * indent + f"({node_type}")

        for value in node_values:
            pretty_print_parse_tree(value, indent + 1)
        print("  " * indent + ")")

    elif isinstance(tree, list):
        print("  " * indent + "[")
        for item in tree:
            pretty_print_parse_tree(item, indent + 1)
        print("  " * indent + "]")
    else:  # Base case: primitive value
        print("  " * (indent + 1) + str(tree))

pretty_print_parse_tree(parse_program())



