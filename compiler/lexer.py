import re

token_specification = [
    ('NUMBER',   r'\d+(\.\d*)?'),  
    ('ASSIGN',   r'='),            
    ('END',      r';'),            
    ('ID',       r'[A-Za-záéíóúÁÉÍÓÚüÜñÑ_][A-Za-z0-9áéíóúÁÉÍÓÚüÜñÑ_]*'),  
    ('OP',       r'[+\-*/><=]'),   
    ('NEWLINE',  r'\n'),           
    ('SKIP',     r'[ \t]+'),       
    ('IF',       r'if\b'),
    ('ELSE',     r'else\b'),
    ('FOR',      r'for\b'),
    ('IN',       r'in\b'),
    ('RANGE',    r'range\b'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('COLON',    r':'),
    ('COMMA',    r','),
    ('QUOTE',    r'"'),
    ('BACKSLASH', r'\\'),
    ('COMMENT',  r'#.*'), 
    ('MISMATCH', r'.'),            
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

def tokenize(code):
    line_num = 1
    line_start = 0
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind == 'SKIP' or kind == 'COMMENT':
            pass  
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} inesperado en la línea {line_num}')
        else:
            tokens.append((kind, value, line_num, column))
    return tokens
