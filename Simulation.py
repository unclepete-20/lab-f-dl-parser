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
        self.dfa_dict = {(pos[0], pos[1]): pos[2] for pos in dfa}

    def simulate(self):
        text = ""
        position = self.start[0]
        for x in self.test:
            for l in x:
                exists = True
                value = ord(l)

                next_position = self.dfa_dict.get((position, str(value)))
                if next_position is not None:
                    text += chr(value)
                    position = next_position
                    exists = False
                else:
                    if exists:
                        if position == self.start[0]:
                            self.result.append(["lexical error", l])
                            text = ""
                        else:
                            indice = self.end.index(position)
                            self.result.append([self.tokens[indice].replace("#", ""), text])
                            text = ""
                            position = self.start[0]

        if text:
            if position == self.start[0]:
                self.result.append(["lexical error", text])
        
        return self.result