# -*-coding:utf-8 -*-
"""
@File    :   Yalex.py
@Date    :   2023/04/25
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase que permite la lectura e interpretacion de los archivos Yalex.
"""

class Definition(object):
    def __init__(self, token_functions):
        self.token_functions = token_functions
        
    def create_python(self):
        with open("Scanner.py", "w") as file:
            file.write("from Token import *\n\n")
            file.write("def scan(token):\n")
            
            for token, code in self.token_functions:
                file.write(f"    if token == '{token}':\n")
                
                if not code:
                    file.write("        return\n")
                else:
                    file.write("        try:\n")
                    file.write(f"            {code}\n")
                    file.write("        except NameError:\n")
                    file.write("            return f'Token indefinido: {{token}}'\n")
            
            file.write("    return f'Token indefinido: {{token}}'\n")
            file.close
