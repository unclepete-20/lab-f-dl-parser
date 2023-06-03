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
from Yalp import Yalp
from Parser import Parser

header = pyfiglet.figlet_format("Y A L E X")
print(header)

yalex = "./yalex/yalp_analyzer.yal"
test_yalex = "./yalex/slr-4.yal"
test_yalp = "./yalp/slr-4.yalp"

with open(test_yalp) as f:
    testLines = f.readlines()

start_time = time.time()

regex, token_functions = Yalex(yalex).read_yalex()


post = Postfix(regex)
postfix = post.shunting_yard()
print("\npostfix: {postfix}\n")


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

dfa.visualize_dfa(direct[0], direct[1], 'yalp_analyzer.yal')


print(f"\ntoken_functions: {token_functions}\n")
    
simulation = Simulation(direct[0], direct[1], testLines)
sim = simulation.simulate()

python_file = Definition(token_functions)
python_file.create_python()
python_file.create_scanner_output()

print(f"\nsimulacion: {sim}\n")


from Scanner import *

output_scanner(sim)

yalp = Yalp(test_yalex, sim)
yalp.init_construction()
yalp.subset_construction()
yalp.show_graph('slr-4')

print(yalp)

test_yalp = "./test/yalp_test.txt"
with open(test_yalp) as f:
    testLines = f.readlines()

    
simulation_yalp = Simulation(direct[0],direct[1],testLines)
test_token = simulation_yalp.simulate()

print(yalp.subsets)

parse = Parser(yalp.transitions, yalp.subsets, yalp.subsets_num, yalp.subproductions)
parse.construct_table()
parse.draw_table()
parse.simulation(test_token)