from Token import *

def scan(token):
    if token == 'ws':
        try:
            return WHITESPACE
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == 'if':
        try:
            return IFSTATEMENT
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == 'id':
        try:
            return ID
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == 'number':
        try:
            return NUMBER
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == '+':
        try:
            return PLUS
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == '-':
        try:
            return MINUS
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == '*':
        try:
            return TIMES
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == '/':
        try:
            return DIV
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == '(':
        try:
            return LPAREN
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == ')':
        try:
            return RPAREN
        except NameError:
            return f'Token indefinido: {{token}}'
    return f'Token indefinido: {{token}}'

def output_scanner(simulation):
    with open('./definition/output_definitions.txt', 'w') as f:
        for s in simulation:
            scanner = scan(s[0])
            f.write(f'{s} ==> Definicion: {scanner}\n')
