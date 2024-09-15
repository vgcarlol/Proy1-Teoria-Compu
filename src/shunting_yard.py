def infix_to_postfix(expression):
    # Lista que actuará como la pila de salida para construir la expresión postfix
    output = []
    # Lista que actuará como la pila de operadores
    operators = []
    # Diccionario que define la precedencia de los operadores. 
    # '*' tiene la precedencia más alta, seguida de '.', luego '|', y '(' con la menor precedencia.
    precedence = {'*': 3, '.': 2, '|': 1, '(': 0}
    
    # Recorrer cada carácter de la expresión regular de entrada
    for char in expression:
        # Si el carácter es un símbolo del alfabeto (letras o dígitos) o es ε (epsilon), agregarlo a la salida
        if char.isalnum() or char == 'ε':
            output.append(char)
        # Si el carácter es '(', se agrega a la pila de operadores
        elif char == '(':
            operators.append(char)
        # Si el carácter es ')', se procesa hasta encontrar '(' en la pila de operadores
        elif char == ')':
            # Sacar operadores de la pila y añadirlos a la salida hasta encontrar '('
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            # Sacar '(' de la pila de operadores, pero no añadirlo a la salida
            operators.pop()
        else:  # Si el carácter es un operador (*, ., |)
            # Mientras haya operadores en la pila y el operador actual tenga una precedencia menor o igual
            # que el operador en el tope de la pila, sacar los operadores de la pila y añadirlos a la salida
            while operators and precedence[char] <= precedence[operators[-1]]:
                output.append(operators.pop())
            # Agregar el operador actual a la pila de operadores
            operators.append(char)
    
    # Al final, sacar todos los operadores restantes de la pila y añadirlos a la salida
    while operators:
        output.append(operators.pop())
    
    # Retornar la expresión postfix como una cadena
    return ''.join(output)
