# -*-coding:utf-8 -*-
'''
@File    :   Simulation.py
@Date    :   2023/04/25
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase Simulation que permite simular un archivo para determinar si pertenece a la gramatica.
'''

class Simulation:
    def __init__(self, dfa, sfPoint, test):
        self.dfa = dfa
        self.start = sfPoint[0]
        self.end = sfPoint[1]
        self.tokens = sfPoint[2]
        self.test = test
        self.result = []
        
    def simulate(self):
        text = ""
        position = self.start[0]
        for x in self.test:
            for l in x:
                done = False
                notExist = True
                val = ord(l)
                while not (done):
                    
                    for pos in self.dfa:
                        if pos[0] == position and pos[1] == str(val):
                            text += chr(val)
                            position = pos[2]
                            notExist = False
                            done = True
                            break
                
                    if notExist:
                        if position == self.start[0]:
                            self.result.append(["lexical error",l])
                            text = ""
                            done = True
                        else:
                            
                            indice = self.end.index(position)
                            self.result.append([self.tokens[indice].replace("#",""),text])
                            text = ""
                            position = self.start[0]

        if text:
            if position == self.start[0]:
                self.result.append(["lexical error",text])
                text = ""
            else:
                indice = self.end.index(position)
                self.result.append([self.tokens[indice].replace("#",""),text])
                text = ""
                position = self.start[0]
            
                        
        return self.result