# -*-coding:utf-8 -*-
"""
@File    :   Yalex.py
@Date    :   2023/04/01
@Author  :   Pedro Arriola (20188)
@Version :   1.0
@Desc    :   Clase que permite la lectura e interpretacion de los archivos Yalex.
"""


class Yalex:
    
    def __init__(self, yalex):
        self.yalex = yalex
    
    def read_yalex(self):
        #aqui se guardaran todos los let
        funciones = []
        filter_funciones = []
        #aqui se guardaran los regex
        regex = []
        filter_regex = []
        #para guardar las palabras y ver que se hara con ello segun la funcion que tengan
        word = ""
        # leer el archivo
        with open(self.yalex, 'r') as yalex:
            lines = yalex.readlines()

        # print(lines)
        # print("==============================")

        active_elements = False

        #obtener los elementos
        for line in lines:
            #obtener los tokens
            if active_elements:
                temporary_word = ""
                for x in line:
                    if x != " " :
                        if x != "\n":
                            if x != "'":
                                temporary_word += x
                            if x =="|":
                                regex.append(temporary_word)
                                temporary_word = ""
                        else:
                            regex.append(temporary_word)
            #obtener todas sus funciones
            if line.startswith("let"):
                funciones.append(line[4:-1])
            #activar lo de tokens
            if line.startswith("rule"):
                active_elements = True
                
        #realizar limpieza de los datos de regex
        for x in range(len(regex)):
            temporary_word = ""
            for l in regex[x]:
                temporary_word += l
                if "{" in temporary_word:
                    temporary_word = temporary_word[:-1]
                    break 
                if "(*" in temporary_word:
                    temporary_word = temporary_word[:-2]
                    break 
            regex[x] = temporary_word

        for x in regex:
            if len(x) != 0:
                if x.count('"') == 2:
                    x = x[1:-1]
                filter_regex.append(x)
        # print("filter_regex: ", filter_regex)
        #limpieza de los datos de funciones

        print(funciones)
        for f in funciones:
            deletable_array = []
            temporal_array = []
            nombre, definicion = f.split("=")
            nombre = nombre.strip()
            definicion = definicion.strip()
            # print("definicion: ", definicion)
            # definicion = definicion.replace('\\t', '\t').replace('\\n', '\n')
            # print("definicion modificada: ", definicion)
            temporal_array.append(nombre)
            # print(temporal_array)
            word= ""
            #realizar revision para a definicion
            if definicion[0] == "[":
                definicion = definicion[1:-1]
                for x in definicion:
                    word+=x
                    if word[0] == '"' or word[0] == "'":
                        if word.count("'") == 2:
                            word = word[1:-1]
                            # print("word: ", word)
                            # print(len(word))
                            #estos son los que tienen \
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
                                    deletable_array.append(ord(word))
                            word = ""
                            # print("deletable_array: ", deletable_array)
                        if word.count('"') == 2:
                            # si tiene \ o no tiene dependiendo de este se trabajara conforme a ello
                            # print("word: ", word)
                            word = word[1:-1]
                            # deletable_array.append(word[1:-1])
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
                                        # print("temp_word: ", ord(temp_word).to_bytes(2, byteorder='little').hex())
                                        # deletable_array.append(ord(temp_word).to_bytes(2, byteorder='little').hex())
                                        word = bytes(temp_word, 'utf-8').decode('unicode_escape')
                                        deletable_array.append(ord(word))
                                        temporary_word = temporary_word[2:]
                                if len(temporary_word) != 0:
                                    if temporary_word == "\s":
                                        temp_word = ' '
                                    else:
                                        temp_word = temporary_word
                                    # print("temp_word: ", ord(temp_word).to_bytes(2, byteorder='little').hex())
                                    # deletable_array.append(ord(temp_word).to_bytes(2, byteorder='little').hex())
                                    word = bytes(temp_word, 'utf-8').decode('unicode_escape')
                                    deletable_array.append(ord(word))
                            else:
                                word = list(word)
                                for w in range(len(word)):
                                    word[w] = ord(word[w])
                                deletable_array.extend(word)
                        # print(deletable_array)
                                
                    else:
                        # print("word: ", word)
                        deletable_array.append(word)
                        word = ""
                    # print("deletable array: ", deletable_array)
                
                # print(definicion)
                
            else:
                # print("word: ", definicion)
                tokens = []
                token_actual = ""
                
                for caracter in definicion:
                    # print("caracter: ",caracter)
                    # print("token_actual: ",token_actual)
                    
                    if "]" in token_actual:
                        palabra = ""
                        array = []
                        array.append("(")
                        
                        token_actual = token_actual[1:-1]
                        # print("token_actual: ",token_actual)
                        for tok in token_actual:
                            palabra += tok
                            if palabra.count("'") == 2:
                                palabra = ord(palabra[1:-1])
                                array.append(palabra)
                                array.append("|")
                                palabra = ""
                        array[len(array)-1] = ")"
                        tokens.extend(array)
                        token_actual = ""
                    
                    if token_actual.count("'") == 2:
                        if "[" not in token_actual:
                            token_actual = token_actual[1:-1]
                            tokens.append(token_actual)
                            token_actual = ""
                    
                    if caracter in ("(", ")", "*", "?", "+", "|","."):
                        if "'" not in token_actual:
                            if token_actual:
                                if len(token_actual) == 1:
                                    token_actual = ord(token_actual)
                                tokens.append(token_actual)
                                token_actual = ""
                            tokens.append(caracter)
                        else:
                            token_actual += caracter
                    else:
                        token_actual += caracter
                    # print("tokens: ", tokens)
                    # print("==================")
                if token_actual:
                    tokens.append(token_actual)
                # print("tokens: ", tokens)
                
                deletable_array.extend(tokens)
                
                
            temporal_array.append(deletable_array)
            
            #agregar temporal array a funciones
            filter_funciones.append(temporal_array)
            # print("filter_funciones antes: ",filter_funciones)
            
            # print(nombre)
            # print(definicion)
        # print("filter_funciones: ", filter_funciones)

        #agregar concatenacion a las funciones
        for x in range(len(filter_funciones)):
            isFunc = True
            
            #revisar si tiene int
            for c in ["+","*","(",")","?","|"]:
                if c in filter_funciones[x][1]:
                    isFunc = False
                
            # print("filter_funciones: ", filter_funciones[x][1])
            # print(isFunc)
            
            if isFunc == False:
                #revisar si tiene .
                
                #comenzar a concatenar
                temporal_array = []
                for y in filter_funciones[x][1]:
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
                            
                filter_funciones[x][1] = temporal_array[:-1]
                
            else:
                #revisar si tiene -
                ascii_array=[]
                newString_Array = []
                if '-' in filter_funciones[x][1]:
                    for z in range(len(filter_funciones[x][1])):
                        if filter_funciones[x][1][z] == '-':
                            for i in range(filter_funciones[x][1][z-1],filter_funciones[x][1][z+1]+1):
                                ascii_array.append(i)
                    #convertir el ascii en string otra vez, en este caso lo dejo como ascii
                    for i in ascii_array:
                        newString_Array.append(i)
                    # print(newString_Array)
                    #reemplazarlo en su respectiva posicion
                    filter_funciones[x][1] = newString_Array
                    #convertir en chr los ascii
                # else:
                #     for z in range(len(filter_funciones[x][1])):
                #         if type(filter_funciones[x][1][z]) == int:
                #             filter_funciones[x][1][z] = chr(filter_funciones[x][1][z])
                            
                #añadir los | en cada uno
                newString_Array = []
                for y in filter_funciones[x][1]:
                    newString_Array.append(y)
                    newString_Array.append('|')
                    
                newString_Array = newString_Array[:-1]
                filter_funciones[x][1] = newString_Array
                
                # print("filter_funciones: ",filter_funciones[x][1])

        #agregar () al final y inicial 
        # print(filter_funciones)
        for func in filter_funciones:
            func[1].insert(0,"(")
            func[1].insert(len(func[1]),")")

        #convertilos en axi solo aquellos que no forman parte de alguna funcion

        # print("===================================")
        # print("funciones:")
        functionNames = []
        #obtener los nombres de las funciones
        for x in filter_funciones:
            functionNames.append(x[0])
            # print(x)
        functionNames.append('|')
        # print("filter_regex: ",filter_regex)
        for x in range(len(filter_regex)):
            if filter_regex[x] not in functionNames:
                if len(filter_regex[x]) == 1:
                    # print("filter_regex[x]: ", filter_regex[x])
                    filter_regex[x] = ord(filter_regex[x])
        
        # print("filter_regex: ",filter_regex)      

        #agregar los #
        temporalNewRegex = []
        for x in filter_regex:
            if x != "|":
                temporalNewRegex.append("(")
                temporalNewRegex.append(x)
                temporalNewRegex.append("•")
                temporalNewRegex.append("#"+str(x))
                temporalNewRegex.append(")")
            else:
                temporalNewRegex.append(x)
        
        # print("temporalNewRegex: ",temporalNewRegex)
        filter_regex = temporalNewRegex        
        # print("\nregex: ", filter_regex)

        #comenzar a reemplazar la regex
        final_regex = []
        for rege in filter_regex:
            existe = False
            #si la regex existe en las funciones
            for func in filter_funciones:
                if rege == func[0]:
                    # print("rege: ",rege)
                    existe = True
                    #este sera en el que tendra todos los cambios y por el cual se cambiara
                    regex_temporal = []
                    regex_temporal.extend(func[1])
                    #seguir revisando si en el regex temporal si dentro de el aun existe valores que pertenecen a las funcioens hasta que ya ninguno no tenga mas
                    largo = 0
                    while (largo != len(regex_temporal)):
                                    
                        largo = len(regex_temporal)
                        # print("regex_temporal: ", regex_temporal)
                        # print("largo: ",largo)   
                        # print("===========")
                        i = 0
                        regex_evaluacion = []
                        while (i < len(regex_temporal)):
                            existe2 = False
                            for x in filter_funciones:
                                if regex_temporal[i] == x[0]:
                                    existe2 = True
                                    # print("regex_temporal[i]: ",regex_temporal[i], i ,len(regex_temporal))
                                    # print("regex_evaluacion fist: ", regex_evaluacion)
                                    regex_evaluacion.extend(x[1])
                                    # print("regex_evaluacion second: ", regex_evaluacion)
                                    regex_evaluacion.extend(regex_temporal[i+1:])
                                    # print("regex_evaluacion last: ", regex_evaluacion)
                                    regex_temporal = regex_evaluacion
                                    # print("regex_temporal modificado: ", regex_temporal)
                                    i = len(regex_temporal)
                                    regex_evaluacion = []
                                    # input()
                                    break

                            if existe2 == False:
                                # print("regex_temporal[i]: ", regex_temporal[i])
                                regex_evaluacion.append(regex_temporal[i])
                                i+=1
                            
                    final_regex.extend(regex_temporal)
            #si la regex no existe en las funciones solo agregarlo
            if existe == False:
                final_regex.append(rege)
            # print("=============================================")
            # print("final_regex: ",final_regex)

        # print("\nfinal regex: ", final_regex)
        return final_regex