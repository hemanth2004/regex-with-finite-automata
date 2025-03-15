from enum import Enum

ignore_chars = [' ', '.']

class TokenType(Enum):
    LPAREN = '('
    RPAREN = ')'
    STAR = '*'
    UNION = '+'
    CONCAT = '.'
    SYMBOL = 'SYMBOL'
    

def is_symbol(char):
    for ignore_char in ignore_chars:
        if ignore_char == char:
            return False
    
    for token in TokenType:
        if token.value == char:
            return False
        
    return True

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        if self.value:
            return f"Token({self.type}, {self.value})"
        return f"Token({self.type})"

    def __repr__(self):
        return self.__str__()