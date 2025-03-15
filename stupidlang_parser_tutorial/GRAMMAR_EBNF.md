<Program> ::= <Statement>*
<Statement> ::= <Print> | <Assignment> | <IfElse> '\n'
<Print> ::= 'print' <Expression>
<Assignment> ::= VAR '<-' <Expression>
<AskInt> ::= 'ask_int' <Expression>
<Expression> ::= STR | INT | VAR | <AskInt>
<IfElse> ::= 'if' <Expression> ('=' | '!=' | '<' | '>') <Expression> <Statement>* ('else' <Statement>*)? 'end'
