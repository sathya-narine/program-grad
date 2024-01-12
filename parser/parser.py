# pa4 parser for the c minus language

#import ply
import ply.lex as lex
import ply.yacc as yacc

# Lexer list of tokens , which are used basically identified as terminals
tokens = (
    'ELSE',
    'EXIT',
    'FLOAT',
    'IF',
    'INT',
    'READ',
    'RETURN',
    'WHILE',
    'WRITE',
    'AND',
    'ASSIGN',
    'CM',
    'DIVIDE',
    'EQ',
    'GE',
    'GT',
    'LBR',
    'LBK',
    'LE',
    'LP',
    'LT',
    'MINUS',
    'NE',
    'NOT',
    'OR',
    'PLUS',
    'RBR',
    'RBK',
    'RP',
    'SC',
    'SQ',
    'TIMES',
    'COMMENT',
    'IDENTIFIER',
    'INTCON',
    'FLOATCON',
    'STRING',
)

# identifying the token, no action is required as comments will be ignored.
def t_COMMENT(t):
    r'/\*(.|\n)*\*/'
    pass
    
def t_ELSE(t):
    r'else'
    return t
def t_EXIT(t):
    r'exit'
    return t
def t_FLOAT(t):
    r'float'
    return t
def t_IF(t):
    r'if'
    return t
def t_INT(t):
    r'int'
    return t
def t_READ(t):
    r'read'
    return t
def t_RETURN(t):
    r'return'
    return t
def t_WHILE(t):
    r'while'
    return t
def t_WRITE(t):
    r'write'
    return t

t_AND = r'&&'
t_ASSIGN = r'='
t_CM = r','
t_DIVIDE = r'/'
t_EQ = r'=='
t_GE = r'>='
t_GT = r'>'
t_LBR = r'{'
t_LBK = r'\['
t_LE = r'<='
t_LP = r'\('
t_LT = r'<'
t_MINUS = r'-'
t_NE = r'!='
t_NOT = r'!'
t_OR = r'\|\|'
t_PLUS = r'\+'
t_RBR = r'}'
t_RBK = r'\]'
t_RP = r'\)'
t_SC = r';'
t_SQ = r'\''
t_TIMES = r'\*'


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'IDENTIFIER' 
    return t

t_ignore = ' \t'

def t_INTCON(t):
    r'\d+'
    t.value = int(t.value)
    return t  
    
def t_FLOATCON(t):
    r'\d+\.\d*|\.\d+'
    t.value = float(t.value)
    return t
    
def t_STRING(t):
    r'\'([a-z]|[A-Z]|[0-9])*\''
    
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
#t_ignore = ' \t\n'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# Parser 
# defining the grammar rules for the language
# https://www.dabeaz.com/ply/
# https://www.youtube.com/watch?v=kearNtiYWr8&t=2863s
        
def p_Program(p):
    ''' Program : DeclList Procedures
                | Procedures
                | DeclList Statement'''
    if len(p)==2:
        p[0] = (p.lineno(1),'Program',p[1])
    else:
        p[0] = (p.lineno(1),'Program',p[1],p[2])
         
def p_Procedures(p):
    ''' Procedures : ProcedureDecl Procedures
                   | ProcedureDecl'''
    if len(p)==2:
        p[0] = (p.lineno(1),'Procedures',p[1])
    else:
        p[0] = (p.lineno(1),'Procedures',p[1],p[2])
    
def p_ProcedureDecl(p):
    ''' ProcedureDecl : ProcedureHead ProcedureBody'''
    p[0]= (p.lineno(1),'ProcedureDecl',p[1],p[2])
    
def p_ProcedureHead(p):
    ''' ProcedureHead : FunctionDecl DeclList
                      | FunctionDecl'''
    if len(p)==2:
        p[0] = (p.lineno(1),'ProcedureHead',p[1])
    else:
        p[0] = (p.lineno(1),'ProcedureHead',p[1],p[2])
    
def p_FunctionDecl(p):
    ''' FunctionDecl : Type IDENTIFIER LP RP LBR'''
    p[0] = (p.lineno(1),'FunctionDecl',p[1],p[2],p[3],p[4],p[5])
    
def p_ProcedureBody(p):
    ''' ProcedureBody : StatementList RBR'''
    p[0] = (p.lineno(1),'ProcedureBody',p[1],p[2])
    
def p_DeclList(p):
    ''' DeclList : Type IdentifierList SC
                 | DeclList Type IdentifierList SC'''
    if len(p)==4:
        p[0] = (p.lineno(1),'DeclList',p[1],p[2],p[3])
    else:
        p[0] = (p.lineno(1),'DeclList',p[1],p[2],p[3],p[4])
    
def p_IdentifierList(p):
    ''' IdentifierList : VarDecl
                       | IdentifierList CM VarDecl'''
    if len(p) == 2:
        p[0] =(p.lineno(1),'IdentifierList',p[1])
    else:
        p[0] = (p.lineno(1),'IdentifierList',p[1],p[2],p[3])
    
def p_VarDecl(p):
    ''' VarDecl : IDENTIFIER
                | IDENTIFIER LBK INTCON RBK'''
    if len(p) == 2:
        p[0] =(p.lineno(1),'VarDecl',p[1])
    else:
        p[0] = (p.lineno(1),'VarDecl',p[1],p[2],p[3],p[4])
    
def p_Type(p):
    ''' Type : INT
             | FLOAT'''
    p[0] = (p.lineno(1),'Type',p[1])
    
def p_StatementList(p):
    ''' StatementList : Statement 
                      | StatementList Statement'''
    if len(p) == 2:
        p[0] =(p.lineno(1),'StatementList',p[1])
    else:
        p[0] = (p.lineno(1),'StatementList',p[1],p[2])
    
def p_Statement(p):
    ''' Statement : Assignment
                  | IfStatement
                  | WhileStatement
                  | IOStatement
                  | ReturnStatement
                  | ExitStatement
                  | CompoundStatement'''
    p[0]=(p.lineno(1),'Statement',p[1])
    
def p_Assignment(p):
    ''' Assignment : Variable ASSIGN Expr SC'''
    p[0]=(p.lineno(1),'Assignment',p[1])
    
def p_IfStatement(p):
    ''' IfStatement : IF TestAndThen ELSE CompoundStatement
                    | IF TestAndThen '''
    if len(p) == 3:
        p[0] =(p.lineno(1),'IfStatement',p[1],p[2])
    else:
        p[0] =(p.lineno(1),'IfStatement',p[1],p[2],p[3],p[4])
    
def p_TestAndThen(p):
    ''' TestAndThen : Test CompoundStatement'''
    p[0] = (p.lineno(1),'TestAndThen',p[1],p[2])
    
def p_Test(p):
    ''' Test : LP Expr RP'''
    p[0] =(p.lineno(1),'Test',p[1],p[2],p[3])
    
def p_WhileStatement(p):
    ''' WhileStatement : WhileToken WhileExpr Statement'''
    p[0] =(p.lineno(1),'WhileStatement',p[1],p[2],p[3])
    
def p_WhileToken(p):
    ''' WhileToken : WHILE'''
    p[0] = (p.lineno(1),'WhileToken',p[1])
    
def p_WhileExpr(p):
    ''' WhileExpr : LP Expr RP'''
    p[0] = (p.lineno(1),'WhileExpr',p[1],p[2],p[3])
    
def p_IOStatement(p):
    ''' IOStatement : READ LP Variable RP SC
                    | WRITE LP Expr RP SC
                    | WRITE LP StringConstant RP SC'''
    p[0] =(p.lineno(1),'IOStatement',p[1],p[2],p[3],p[4],p[5])
    
def p_ReturnStatement(p):
    ''' ReturnStatement : RETURN Expr SC'''
    p[0] =(p.lineno(1),'ReturnStatement',p[1],p[2],p[3])
    
def p_ExitStatement(p):
    ''' ExitStatement : EXIT SC'''
    p[0] =(p.lineno(1),'ExitStatement',p[1],p[2])
    
def p_CompoundStatement(p):
    ''' CompoundStatement : LBR StatementList RBR'''
    p[0] =(p.lineno(1),'CompoundStatement',p[1],p[2],p[3])
    
def p_Expr(p):
    ''' Expr : Expr AND SimpleExpr
             | Expr OR SimpleExpr
             | SimpleExpr
             | NOT SimpleExpr'''
    if len(p) == 2:
        p[0] =(p.lineno(1),'Expr',p[1])
    elif len(p) == 3:
        p[0] =(p.lineno(1),'Expr',p[1],p[2])
    else:
        p[0] =(p.lineno(1),'Expr',p[1],p[2],p[3])
        
def p_SimpleExpr(p):
    ''' SimpleExpr : SimpleExpr EQ AddExpr
                   | SimpleExpr NE AddExpr
                   | SimpleExpr LE AddExpr
                   | SimpleExpr LT AddExpr
                   | SimpleExpr GE AddExpr
                   | SimpleExpr GT AddExpr
                   | AddExpr'''
    if len(p) == 2:
        p[0] =(p.lineno(1),'SimpleExpr',p[1])
    else:
        p[0] =(p.lineno(1),'SimpleExpr',p[1],p[2],p[3])
    
def p_AddExpr(p):
    ''' AddExpr : AddExpr PLUS MulExpr
                | AddExpr MINUS MulExpr
                | MulExpr'''
    if len(p) == 2:
        p[0] =(p.lineno(1),'AddExpr',p[1])
    else:
        p[0] =(p.lineno(1),'AddExpr',p[1],p[2],p[3])
    
def p_MulExpr(p):
    '''MulExpr : MulExpr TIMES Factor
               | MulExpr MINUS Factor
               | Factor'''
    if len(p) == 2:
        p[0] =(p.lineno(1),'MulExpr',p[1])
    else:
        p[0] =(p.lineno(1),'MulExpr',p[1],p[2],p[3])
    
def p_Factor(p):
    ''' Factor : Variable
               | Constant
               | IDENTIFIER LP RP
               | LP Expr RP'''
    if len(p) == 2:
        p[0] =(p.lineno(1),'Factor',p[1])
    else:
        p[0] =(p.lineno(1),'Factor',p[1],p[2],p[3])
    
def p_Variable(p):
    ''' Variable : IDENTIFIER
                 | IDENTIFIER LBK Expr RBK'''
    if len(p) == 2:
        p[0] =(p.lineno(1),'Variable',p[1])
    else:
        p[0] =(p.lineno(1),'Variable',p[1],p[2],p[3],p[4])
    
def p_StringConstant(p):
    ''' StringConstant : STRING'''
    p[0] =(p.lineno(1),'StringConstant',p[1])
    
def p_Constant(p):
    ''' Constant : INTCON
                 | FLOATCON'''
    p[0] =(p.lineno(1),'Constant',p[1])
    
def p_error(p):
    if p:
         print(p)
         print("ERROR: ",p.lineno -2, ": Parser: parse error near ",p.type)
    else:
         print("Syntax error at EOF")

# creating a parser
parser = yacc.yacc()

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
    
print('\nTokens List')
print(token_list)
# pass the source code to parser
result = parser.parse(data)

# This function takes the tuple as input and prints
# in tree structure 
# https://simonhessner.de/python-3-recursively-print-structured-tree-including-hierarchy-markers-using-depth-first-search/
def printTree(node, markerStr="+- ", levelMarkers=[]):
    emptyStr = " " * len(markerStr)
    connectionStr = "|" + emptyStr[:-1]

    level = len(levelMarkers)
    mapper = lambda draw: connectionStr if draw else emptyStr
    markers = "".join(map(mapper, levelMarkers[:-1]))
    markers += markerStr if level > 0 else ""

    if isinstance(node, tuple):
        print(f"{markers}{node[1]}")

        for i, child in enumerate(node[2:]):
            isLast = i == len(node) - 3
            printTree(child, markerStr, [*levelMarkers, not isLast])
    else:
        print(f"{markers}{node}")
                
if result:
    print('\nParsing Succssfull')
    # Print the tree
    print('Parse Tree:')
    printTree(result)
else:
    print('Found one or more errors during parsing')