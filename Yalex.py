# -*-coding:utf-8 -*-
"""
@File    :   Yalex.py
@Date    :   2023/04/25
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase que permite la lectura e interpretacion de los archivos Yalex.
"""


class Yalex:
    
    def __init__(self, yalex):
        self.yalex = yalex
    
    def read_yalex(self):
        funciones = []
        filter_functions = []
        regex = []
        filter_regex = []
        token_regex = []
        token_functions = []
        word = ""
        
        # Se lee el archivo
        with open(self.yalex, 'r') as yalex:
            lines = yalex.read()

        activeRule = False
        #separarlos por let o rule
        for l in lines:
            if activeRule:
                if l == "|":
                    if word != "":
                        word=""
                    regex.append(l.strip())
                else:
                    if l not in ["\n",'\t'] : 
                        word += l
                        if "{" in word and "}" in word:
                            word = word.strip()
                            regex.append(word)
                            word = ""
                        if "(*" in word and "*)" in word:
                            word = ""
                    elif l == "\n":
                        # print("word: ", word)
                        if word:
                            if "{" not in word:
                                word = word.strip()
                                if word != "":
                                    regex.append(word)
                        word+=" "
            else:
                word+=l
                
                if '\n' in word:
                    if len(word) > 0:
                        if "let" in word:
                            word = word.strip()
                            word = word[3:].strip()
                            funciones.append(word)
                        if "rule" in word: 
                            activeRule = True
                        word = ""
        
        regex = list(filter(bool, regex))
        
        #obtener los tokens
        for x in range(len(regex)):
            temporary_array = []
            temporary_word = ""
            token_active = False
            for l in regex[x]:
                if token_active:
                    if l == "}":
                        temporary_word = temporary_word.replace("'","").replace('"',"").strip()
                        temporary_array.append(temporary_word)
                        token_regex.append(temporary_array[0])
                        token_regex.append("|")
                        temporary_word = ""
                        token_functions.append(temporary_array)
                        break
                    temporary_word += l
                else:
                    temporary_word += l
                if l == "{":
                    temporary_word = temporary_word[:-1].replace("'","").replace('"',"").strip()
                    temporary_array.append(temporary_word)
                    temporary_word = ""
                    token_active = True

            if temporary_word and "|" not in temporary_word and len(temporary_word) > 0:
                temporary_word = temporary_word.strip()
                temporary_array.append(temporary_word)
                temporary_array.append("")
                token_regex.append(temporary_array[0])
                token_regex.append("|")
                token_functions.append(temporary_array)


        token_regex.pop()
                
        #realizar limpieza de los datos de regex
        for x in range(len(regex)):
            temporary_word = ""
            for l in regex[x]:
                temporary_word += l
                if "{" in temporary_word:
                    temporary_word = temporary_word[:-1].strip()
                    break 
                if "(*" in temporary_word:
                    temporary_word = temporary_word[:-2].strip()
                    break 
            if temporary_word.count("'") == 2:
                temporary_word = temporary_word[1:-1]

            regex[x] = temporary_word
        
        for x in regex:
            if len(x) != 0:
                if x.count('"') == 2:
                    x = x[1:-1]
                filter_regex.append(x)


        #limpieza de los datos de funciones
        for f in funciones:
            deletable_array = []
            temporal_array = []
            nombre, definicion = f.split("=")
            nombre = nombre.strip()
            definicion = definicion.strip()

            temporal_array.append(nombre)

            word= ""
            #realizar revision para a definicion
            if definicion[0] == "[":
                definicion = definicion[1:-1]
                for x in definicion:
                    word += x
                    if word[0] == '"' or word[0] == "'":
                        if word.count("'") == 2:
                            word = word[1:-1]

                            if len(word) == 2:
                                if word == "\s":
                                    word = bytes(' ', 'utf-8').decode('unicode_escape')
                                else:
                                    word = bytes(word, 'utf-8').decode('unicode_escape')
                                deletable_array.append(ord(word))
                            #esto son los que no tienen \
                            else:
                                if word == " ":
                                    word = bytes(' ', 'utf-8').decode('unicode_escape')
                                    deletable_array.append(ord(word))
                                else:
                                    print(word)
                                    deletable_array.append(ord(word))
                            word = ""

                        if word.count('"') == 2:
                            word = word[1:-1]
                            temporary_word = ""
                            #si tiene \ en word
                            if chr(92) in word:
                                for y in word:
                                    temporary_word+=y
                                    if temporary_word.count(chr(92)) == 2:
                                        if temporary_word[:-1] == "\s":
                                            temp_word = ' '
                                        else:
                                            temp_word = temporary_word[:-1]
                                        
                                        word = bytes(temp_word, 'utf-8').decode('unicode_escape')
                                        deletable_array.append(ord(word))
                                        temporary_word = temporary_word[2:]
                                if len(temporary_word) != 0:
                                    if temporary_word == "\s":
                                        temp_word = ' '
                                    else:
                                        temp_word = temporary_word

                                    word = bytes(temp_word, 'utf-8').decode('unicode_escape')
                                    deletable_array.append(ord(word))
                            else:
                                word = list(word)
                                for w in range(len(word)):
                                    word[w] = ord(word[w])
                                deletable_array.extend(word)
                                
                    else:
                        deletable_array.append(word)
                        word = ""
                
            else:
                tokens = []
                token_actual = ""
                
                for caracter in definicion:
                    
                    if "]" in token_actual:
                        word = ""
                        array = []
                        array.append("(")
                        
                        token_actual = token_actual[1:-1]
                        for tok in token_actual:
                            word += tok
                            if word.count("'") == 2:
                                word = ord(word[1:-1])
                                array.append(word)
                                array.append("|")
                                word = ""
                        array[len(array)-1] = ")"
                        tokens.extend(array)
                        token_actual = ""
                    
                    if token_actual.count("'") == 2:
                        if "[" not in token_actual:
                            token_actual = ord(token_actual[1:-1])
                            tokens.append(token_actual)
                            token_actual = ""
                    
                    if caracter in ("(", ")", "*", "?", "+", "|","."):
                        if "'" not in token_actual:
                            if token_actual:
                                if len(token_actual) == 1:
                                    token_actual = ord(token_actual)
                                tokens.append(token_actual)
                                token_actual = ""
                            if caracter == ".":
                                caracter = ord(caracter)
                            tokens.append(caracter)
                        else:
                            token_actual += caracter.strip()
                    else:
                        token_actual += caracter.strip()
                if token_actual:
                    tokens.append(token_actual)
                
                deletable_array.extend(tokens)
                
                
            temporal_array.append(deletable_array)
            
            #agregar temporal array a funciones
            filter_functions.append(temporal_array)

        #agregar concatenacion a las funciones
        for x in range(len(filter_functions)):
            isFunc = True
            
            #revisar si tiene int
            for c in ["+","*","(",")","?","|"]:
                if c in filter_functions[x][1]:
                    isFunc = False
                
            
            if isFunc == False:
                #revisar si tiene .
                
                #comenzar a concatenar
                temporal_array = []
                for y in filter_functions[x][1]:
                    temporal_array.append(y)
                    temporal_array.append("•")
                #eliminar las concatenaciones inecesarios del funciones
                for z in range(len(temporal_array)):
                    if temporal_array[z] == "(":
                        if temporal_array[z+1] == "•":
                            temporal_array[z+1] = ''
                    if temporal_array[z] == ")":
                        if temporal_array[z-1] == "•":
                            temporal_array[z-1] = ''
                    if temporal_array[z] == "*":
                        if temporal_array[z-1] == "•":
                            temporal_array[z-1] = ''
                    if temporal_array[z] == "|":
                        if temporal_array[z-1] == "•":
                            temporal_array[z-1] = ''
                        if temporal_array[z+1] == "•":
                            temporal_array[z+1] = ''
                    if temporal_array[z] == "+":
                        if temporal_array[z-1] == "•":
                            temporal_array[z-1] = ''
                    if temporal_array[z] == "?":
                        if temporal_array[z-1] == "•":
                            temporal_array[z-1] = ''
                temporal_array = [element for element in temporal_array if element != '']
                            
                filter_functions[x][1] = temporal_array[:-1]
                
            else:
                #revisar si tiene -
                ascii_array=[]
                newString_Array = []
                if '-' in filter_functions[x][1]:
                    for z in range(len(filter_functions[x][1])):
                        if filter_functions[x][1][z] == '-':
                            for i in range(filter_functions[x][1][z-1],filter_functions[x][1][z+1]+1):
                                ascii_array.append(i)
                    #convertir el ascii en string otra vez, en este caso lo dejo como ascii
                    for i in ascii_array:
                        newString_Array.append(i)
                    #reemplazarlo en su respectiva posicion
                    filter_functions[x][1] = newString_Array

                #añadir los | en cada uno
                newString_Array = []
                for y in filter_functions[x][1]:
                    newString_Array.append(y)
                    newString_Array.append('|')
                    
                newString_Array = newString_Array[:-1]
                filter_functions[x][1] = newString_Array
                
        for func in filter_functions:
            func[1].insert(0,"(")
            func[1].insert(len(func[1]),")")
            
        functionNames = []
        #obtener los nombres de las funciones
        for x in filter_functions:
            functionNames.append(x[0])

        functionNames.append('|')
        for x in range(len(filter_regex)):
            if filter_regex[x] not in functionNames:
                if len(filter_regex[x]) == 1:
                    filter_regex[x] = ord(filter_regex[x])
   

        #agregar los #
        temporalNewRegex = []
        for x in range(len(filter_regex)):
            if filter_regex[x] != "|":
                temporalNewRegex.append("(")
                temporalNewRegex.append(filter_regex[x])
                temporalNewRegex.append("•")
                temporalNewRegex.append("#"+str(token_regex[x]))
                temporalNewRegex.append(")")
            else:
                temporalNewRegex.append(filter_regex[x])
        
        filter_regex = temporalNewRegex        

        def replace_recursive(reg):
            for func in filter_functions:
                if reg == func[0]:
                    return [item for sublist in [replace_recursive(x) for x in func[1]] for item in sublist]
            return [reg]
    
        final_regex = [item for sublist in [replace_recursive(reg) for reg in filter_regex] for item in sublist]


        return final_regex, token_functions