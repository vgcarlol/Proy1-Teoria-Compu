def read_input(file_path):
    # Inicializar una lista para almacenar las expresiones regulares y las cadenas de entrada
    expressions = []
    
    # Abrir el archivo especificado para leer su contenido
    with open(file_path, 'r') as file:
        # Recorrer cada línea del archivo
        for line in file:
            # Eliminar los espacios en blanco al principio y al final de la línea
            line = line.strip()
            
            # Verificar si la línea contiene una coma, que separa la expresión regular y la cadena
            if ',' in line:
                # Dividir la línea en dos partes: expresión regular (regex) y cadena (string)
                regex, string = line.split(',', 1)
                
                # Eliminar los espacios en blanco alrededor de la expresión regular y la cadena
                regex = regex.strip()
                string = string.strip()
                
                # Agregar la tupla (expresión regular, cadena) a la lista de expresiones
                expressions.append((regex, string))
    
    # Retornar la lista de expresiones y cadenas
    return expressions
