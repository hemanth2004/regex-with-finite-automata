from .tokens import TokenType
from app.ds.ast import ASTNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def _current_token(self):
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def _advance(self):
        self.pos += 1

    def parse(self):
        return self.parse_expression()

    def parse_expression(self):
        terms = []
        
        # Parse first term
        terms.append(self.parse_term())
        
        # Keep parsing terms while we see SYMBOL, LPAREN, or UNION
        while True:
            token = self._current_token()
            if token is None or token.type == TokenType.RPAREN:
                break
            
            if token.type == TokenType.UNION:
                self._advance()
                terms.append(self.parse_term())
                # Create UNION node immediately
                last_two = terms[-2:]
                terms = terms[:-2]
                terms.append(ASTNode("UNION", None, last_two))
            elif token.type in [TokenType.SYMBOL, TokenType.LPAREN]:
                terms.append(self.parse_term())
            else:
                break
        
        # Build concatenation tree from right to left
        while len(terms) > 1:
            right = terms.pop()
            left = terms.pop()
            terms.append(ASTNode("CONCAT", None, [left, right]))
        
        return terms[0]

    def parse_term(self):
        # Parse a factor and handle any postfix operators
        left = self.parse_factor()

        while True:
            token = self._current_token()
            if token is None:
                break

            if token.type == TokenType.STAR:
                self._advance()
                left = ASTNode("STAR", None, [left])
            else:
                break

        return left

    def parse_factor(self):
        token = self._current_token()
        
        if token is None:
            raise SyntaxError("Unexpected end of input")

        if token.type == TokenType.SYMBOL:
            self._advance()
            return ASTNode("SYMBOL", token.value)
        elif token.type == TokenType.LPAREN:
            self._advance()
            expr = self.parse_expression()
            if self._current_token() is None or self._current_token().type != TokenType.RPAREN:
                raise SyntaxError("Expected closing parenthesis")
            self._advance()
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {token}")


