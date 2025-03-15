from .tokens import (
    Token, TokenType, ignore_chars, is_symbol
)


class Lexer:
    def __init__(self, regex):
        self.regex = regex
        self.pos = 0

    def _current_char(self):
        if self.pos >= len(self.regex):
            return None
        return self.regex[self.pos]

    def _advance(self):
        self.pos += 1

    def _preprocess_regex(self):
        self.regex = self.regex.replace(' ', '')
        self.regex = self.regex.replace('\t', '')

    def tokenize(self):
        self._preprocess_regex()
        self.tokens = []
        self.pos = 0

        while self.pos < len(self.regex):
            char = self._current_char()
            
            # Check if char matches any token type
            token_found = False
            for token_type in TokenType:
                if token_type.value == char:
                    self.tokens.append(Token(token_type))
                    token_found = True
                    break
            
            # If no token type matched, it's either a symbol or ignored
            if not token_found:
                if char not in ignore_chars:
                    self.tokens.append(Token(TokenType.SYMBOL, char))
            
            self._advance()

        return self.tokens
