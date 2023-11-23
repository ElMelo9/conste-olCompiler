TOKENS = {
    'SEMICOLON': r';',
    'TYPE': r'\b(Entero|Real|Texto)\b',
    'TEXT': r'"[^"]*"',  # Cadena de texto entre comillas
    'REAL': r'\d+\.\d+',  # Números reales
    'ENTERO': r'\d+',  # Números enteros
    'IDENTIFIER': r'[a-zA-Z_]\w*',  # Identificadores
    'ASSIGNMENT': r'=',
    'METHOD_CALL': r'Captura\.(Texto|Entero|Real)\(([^)]+)\)',
    'PRINT_CALL': r'Mensaje\.Texto\(([^)]+)\)'
}




    

