# -*-coding:utf-8 -*-
'''
@File    :   main.py
@Date    :   2023/04/25
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Main donde se ejecuta toda la logica implementada.
'''

import time
from Postfix import Postfix
import pyfiglet
from Yalex import Yalex
from SyntacticTree import SyntacticTree
from DFA import DFA
from Definition import Definition
from Simulation import Simulation

header = pyfiglet.figlet_format("Y A L E X")
print(header)

yalex = "./yalex/slr-0.yal"

start_time = time.time()

regex, token_functions = Yalex(yalex).read_yalex()

post = Postfix(regex)
postfix = post.shunting_yard()
print("\npostfix: ", postfix)


tree = SyntacticTree(yalex)
tree.tree_construction(postfix)
tree.visualize_tree()

result = tree.left_most()

time.sleep(1)
end_time = time.time()

total_time = end_time - start_time

print("\n===========================================================================================")

print(f"\nLa construccion del arbol sintactico tuvo un tiempo de ejecucion de {total_time} segundos\n")

print("===========================================================================================\n")


# Parte del laboratorio D

dfa = DFA(result)
direct= dfa.Dstate()

dfa.visualize_dfa(direct[0],direct[1])

test = "./test/test.txt"
with open(test) as f:
    testLines = f.readlines()

print("token_functions: ", token_functions)
    
simulation = Simulation(direct[0], direct[1], testLines)
sim = simulation.simulate()

python_file = Definition(token_functions)
python_file.create_python()

print(f"simulacion: {sim}")


from Scanner import *

with open("./definition/output_definitions.txt", "w") as f:
    for s in sim:
        scanner = scan(s[0])
        f.write(f"{s}:{scanner}\n")