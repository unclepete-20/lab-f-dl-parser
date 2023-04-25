from Token import *

def scan(token):
    if token == 'ws':
        try:
            return NONE
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == 'id':
        try:
            if t.value == 0: return ID else: return NONE
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == '+':
        try:
            return PLUS
        except NameError:
            return f'Token indefinido: {{token}}'
    if token == '*':
        try:
            return TIMES
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
    if token == '*)':
        try:
            return STARTCOMMENT
        except NameError:
            return f'Token indefinido: {{token}}'
    return f'Token indefinido: {{token}}'
