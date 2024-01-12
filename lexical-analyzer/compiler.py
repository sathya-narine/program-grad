import ply.lex as lex

#declaring token class names
tokens = (
    'IDENTIFIER',  # variables
    'KEYWORD',     # reserved words
    'CONSTANT',    # constants
    'ARITHMETIC_OP',     # arithmetic operator
    'LOGICAL_OP',        # logical operator
    'SEPARATOR',         # separator
    'COMMENT',           # multi-line comment 
    'MISSING_COMMENT',   # missing close comments
)

# defining the regular expression for multi-line comment
def t_COMMENT(t):
    r'/\*(.|\n)*\*/'
    return t

# defining the regular expression to catch the missing end comment
def t_MISSING_COMMENT(t):
    r'/\*(.|\n)*'
    return t

# defining list of keywords in the regular expression    
def t_KEYWORD(t):
    r'int|float|if|else|exit|while|read|write|return'
    return t

# defining the regular expression for indentifier
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t
    
# handling the invalid identifier
def t_identifier_error(t):
    r'\d+[a-zA-Z_][a-zA-Z0-9_]*|[a-zA-Z0-9_]*[^a-zA-Z0-9_]^'
    print("Invalid Identifier '%s'" % t.value)
    t.lexer.skip(1)

# defining the regular expression for numeric constants    
def t_CONSTANT(t):
    r'\d+\.\d+|\d+'
    return t
        
# defining the regular expressions for arithmetic operators
t_ARITHMETIC_OP = r'\+|-|\*|/|='

# defining the regular expressions for logical operators
t_LOGICAL_OP = r'==|!=|<|>|<=|>=|&&|\|\|'

# defining the separator characters
t_SEPARATOR = r',|;|\(|\)|{|}'

# ignores the new line and tab spaces
t_ignore = ' \t\n' 

# finite state if it doesn't match the lexeme for any accepting state 
# will be caught as error    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Create the lexer
lexer = lex.lex()

if __name__ == '__main__':
    # open the file and read the content
    fh = open("source_code.txt","r")
    data = fh.read()
    print('Source Code:')
    print(data)
    # build the lexer
    lexer.input(data)
    
    # Token list to store tokens
    token_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        token_list.append((tok.type,tok.value))
    print('Tokens List')
    print(token_list)
