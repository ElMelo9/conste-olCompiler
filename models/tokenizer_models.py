import re
class Tokenizer:
    def __init__(self, rules):
        self.rules = sorted([(key, re.compile(pattern)) for key, pattern in rules.items()], key=lambda x: x[0], reverse=True)
        self.variables = {}

    def tokenize(self, text):
        tokens = []
        while text:
            text = text.lstrip()  # Elimina espacios en blanco al inicio
            matched = False
            for name, pattern in self.rules:
                match = pattern.match(text)
                if match:
                    token_value = match.group(0)
                    tokens.append((name, token_value))
                    text = text[match.end():]
                    matched = True
                    break
            if not matched:
                raise ValueError(f"Error tokenizando en la línea: '{text}'")
        return tokens

    def es_declaracion_valida(self, tokens):
        if len(tokens) != 3:
            return {"consola": "", "logs": "Error en la declaración"}

        if tokens[0][0] == 'IDENTIFIER' and tokens[1][0] == 'TYPE' and tokens[2][0] == 'SEMICOLON':
            variable = tokens[0][1]
            tipo_variable = tokens[1][1]  # Obtener el tipo de la variable de los tokens

            # Almacenar la variable con su tipo y un valor inicial
            self.variables[variable] = {'tipo': tipo_variable, 'valor': None}
            return {"consola": "", "logs": "Declaración válida"}

        return {"consola": "", "logs": "Error en la declaración"}

    def es_asignacion_valida(self, tokens, TOKENS):
        if len(tokens) != 4:
            return {"consola": "", "logs": "Error en la asignación"}

        ident, assign, valor, semi = tokens
        if ident[0] == 'IDENTIFIER' and assign[0] == 'ASSIGNMENT' and semi[0] == 'SEMICOLON':
            variable = ident[1]
            if variable not in self.variables:
                return {"consola": "", "logs": f"Error: Variable '{variable}' no ha sido declarada."}

            tipo_variable = self.variables[variable]['tipo']

            # Verificar el tipo de asignación y el tipo de valor
            if valor[0] == 'METHOD_CALL':
                tipo_metodo, valor_metodo = re.match(TOKENS['METHOD_CALL'], valor[1]).groups()

                # Verificar si el tipo del método coincide con el tipo de la variable
                if tipo_metodo != tipo_variable:
                    return {"consola": "", "logs": f"Error en la línea: Tipo de dato no coincide para {variable}. Esperado: {tipo_variable}, Obtenido: {tipo_metodo}"}

                # Validaciones adicionales según el tipo del método
                if tipo_metodo == 'Entero' and not re.fullmatch(TOKENS['ENTERO'], valor_metodo):
                    return {"consola": "", "logs": f"Error Captura.Entero: argumento inválido"}
                elif tipo_metodo == 'Real' and not re.fullmatch(TOKENS['REAL'], valor_metodo):
                    return {"consola": "", "logs": f"Error Captura.Real: argumento inválido"}
                elif tipo_metodo == 'Texto' and not re.fullmatch(TOKENS['TEXT'], valor_metodo):
                    return {"consola": "", "logs": f"Error Captura.Texto: argumento inválido"}

                self.variables[variable]['valor'] = valor_metodo.strip('"')
                return {"consola": "", "logs": "Asignación válida"}
            else:
                # Validación para asignaciones directas según el tipo de la variable
                tipo_variable = self.variables[variable]['tipo']
                if tipo_variable == 'Texto' and not re.fullmatch(TOKENS['TEXT'], valor[1]):
                    return {"consola": "", "logs": f"Error en la línea: se esperaba una cadena de texto para {variable}"}
                elif tipo_variable == 'Entero' and not re.fullmatch(TOKENS['ENTERO'], valor[1]):
                    return {"consola": "", "logs": f"Error en la línea: se esperaba un entero para {variable}"}
                elif tipo_variable == 'Real' and not re.fullmatch(TOKENS['REAL'], valor[1]):
                    return {"consola": "", "logs": f"Error en la línea: se esperaba un real para {variable}"}

                self.variables[variable]['valor'] = valor[1].strip('"')
                return {"consola": "", "logs": "Asignación válida"}

        return {"consola": "", "logs": "Error en la asignación"}

    def analizar_declaraciones(self, texto, TOKENS):
        lineas = texto.strip().split('\n')
        resultados = []
        numero_linea = 1  # Iniciar el conteo de líneas

        for linea in lineas:
            try:
                tokens = self.tokenize(linea.strip())
                if tokens:
                    resultado_linea = self.procesar_linea(tokens, TOKENS)
                    resultados.append({"linea": numero_linea, "texto": linea, "resultado": resultado_linea})
                else:
                    resultados.append({"linea": numero_linea, "texto": linea, "resultado": {"consola": "Línea vacía o no reconocida", "logs": ""}})
            except ValueError as e:
                resultados.append({"linea": numero_linea, "texto": linea, "resultado": {"consola": "", "logs": str(e)}})
                break  # Detener el análisis al encontrar el primer error
            numero_linea += 1

        return resultados

    def es_llamada_impresion_valida(self, tokens, TOKENS):
        if len(tokens) != 2:
            return {"consola": "", "logs": "Error en la llamada de impresión"}

        print_call, semi = tokens
        if print_call[0] != 'PRINT_CALL' or semi[0] != 'SEMICOLON':
            return {"consola": "", "logs": "Error en la llamada de impresión"}

        argumento_match = re.match(TOKENS['PRINT_CALL'], print_call[1])
        if argumento_match:
            argumento = argumento_match.group(1)

            # Distinguir entre una cadena literal y una variable
            if argumento.startswith('"') and argumento.endswith('"'):
                # Es una cadena literal
                valor_impresion = argumento.strip('"')
            elif argumento in self.variables:
                # Es una variable, obtener solo el valor
                valor_impresion = self.variables[argumento]['valor']  # Asumiendo que cada variable es un diccionario
            else:
                return {"consola": "", "logs": f"Error: Variable '{argumento}' no ha sido declarada o asignada."}

            return {"consola": valor_impresion, "logs": "Llamada de impresión válida"}
        else:
            return {"consola": "", "logs": "Error en la llamada de impresión"}
   
    def procesar_linea(self, tokens, TOKENS):
        respuesta = {"consola": "", "logs": ""}

        if tokens[0][0] == 'IDENTIFIER':
            if len(tokens) == 3 and tokens[1][0] == 'TYPE' and tokens[2][0] == 'SEMICOLON':
                # Procesamiento para declaraciones
                resultado = self.es_declaracion_valida(tokens)
            elif len(tokens) == 4 and tokens[1][0] == 'ASSIGNMENT':
                # Procesamiento para asignaciones
                resultado = self.es_asignacion_valida(tokens, TOKENS)
            else:
                resultado = {"consola": "", "logs": "Error en la línea"}
        elif tokens[0][0] == 'PRINT_CALL':
            # Procesamiento para llamadas de impresión
            resultado = self.es_llamada_impresion_valida(tokens, TOKENS)
        else:
            resultado = {"consola": "", "logs": "Error: Declaración no válida"}

        # Asegurarse de que ambos, consola y logs, son cadenas
        consola_resultado = resultado.get("consola", "")
        logs_resultado = resultado.get("logs", "")

        respuesta["consola"] += consola_resultado if consola_resultado is not None else ""
        respuesta["logs"] += logs_resultado if logs_resultado is not None else ""

        return respuesta

