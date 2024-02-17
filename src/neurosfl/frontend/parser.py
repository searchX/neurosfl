# ------------------------------------------------------------
# parser.py
#
# Parses input strings into tokens
# ------------------------------------------------------------
from ply import lex, yacc
from .structs import Node, UnaryOp, StringLiteral, NumberLiteral, StartNode, LogicalOp, ComparisonOp

reserved_words = {
    'where': 'START_WHERE',
    'and': 'AND_OPERATOR',
    'or': 'OR_OPERATOR',
    'not': 'NOT_OPERATOR',
}

# List of token names.   This is always required
tokens = [
    'FIELD_NAME',
    'STRING_LITERAL',
    'NUMBER_LITERAL',
    'COMPARISON_OPERATOR',
    'LEFT_PARENTHESES',
    'RIGHT_PARENTHESES',
] + list(reserved_words.values())

# Regular expression rules for simple tokens
t_COMPARISON_OPERATOR = r'=|!=|>=|<=|>|<'
t_LEFT_PARENTHESES  = r'\('
t_RIGHT_PARENTHESES  = r'\)'

# Match a field name, if it is a reserved word, return the token type
def t_FIELD_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.value = t.value.lower().strip()
    if t.value in reserved_words:
        t.type = reserved_words[t.value]
    else:
        t.value = t.value.lower().strip()
    return t

# Define number literal
def t_NUMBER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define string literal as anything between quotes (single or double)
def t_STRING_LITERAL(t):
    r'\".*?\"|\'.*?\''
    t.value = t.value[1:-1]
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import re
lexer = lex.lex() # ignore case

# Parsing rules
precedence = (
    ('left', 'OR_OPERATOR'),
    ('left', 'AND_OPERATOR'),
    ('nonassoc', 'COMPARISON_OPERATOR'),
    ('nonassoc', 'NOT_OPERATOR'),
    ('left', 'LEFT_PARENTHESES', 'RIGHT_PARENTHESES'),
)

def p_start_where(p):
    '''start : START_WHERE expression
             | expression'''
    if len(p) == 3:
        p[0] = StartNode(p[2])
    else:
        p[0] = StartNode(p[1])

# Parsing
def p_binary_operators(p):
    '''expression :   expression OR_OPERATOR expression
                    | expression AND_OPERATOR expression'''
    p[0] = LogicalOp(p[1], p[2], p[3])

def p_expr_field(p):
    '''expression :   FIELD_NAME COMPARISON_OPERATOR number_value
                    | FIELD_NAME COMPARISON_OPERATOR string_value'''
    p[0] = ComparisonOp(p[1], p[2], p[3])

def p_number_literal(p):
    'number_value : NUMBER_LITERAL'
    p[0] = NumberLiteral(p[1])

def p_string_literal(p):
    'string_value : STRING_LITERAL'
    p[0] = StringLiteral(p[1])

def p_expression_group(p):
    'expression : LEFT_PARENTHESES expression RIGHT_PARENTHESES'
    p[0] = p[2]

def p_error(t):
    if t is None: # lexer error
        return
    print(f"Syntax Error: {t.value!r}")

parser = yacc.yacc()
