def epsilon_closure(states):
    # Inicializar la pila con los estados de entrada y el conjunto de la clausura epsilon con los mismos estados
    stack = list(states)
    closure = set(states)
    print(f"  Calculando clausura epsilon para estados: {[str(id(state)) for state in states]}")

    # Mientras haya estados en la pila, procesar cada uno
    while stack:
        state = stack.pop()  # Tomar el estado del tope de la pila
        # Recorrer las transiciones epsilon del estado actual
        for next_state in state.epsilon_transitions:
            # Si el estado alcanzable no está ya en la clausura, añadirlo
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)  # Añadir el nuevo estado a la pila para procesar sus transiciones epsilon
                print(f"    Añadiendo estado {id(next_state)} a la clausura epsilon")

    print(f"  Clausura epsilon resultante: {[str(id(state)) for state in closure]}")
    return closure  # Retornar el conjunto de la clausura epsilon

def move(states, symbol):
    # Inicializar un conjunto para los estados alcanzables con el símbolo dado
    next_states = set()
    print(f"  Intentando mover con símbolo '{symbol}' desde los estados: {[str(id(state)) for state in states]}")
    
    # Recorrer cada estado en el conjunto actual
    for state in states:
        # Si el estado tiene una transición con el símbolo, procesar las transiciones
        if symbol in state.transitions:
            for next_state in state.transitions[symbol]:
                next_states.add(next_state)  # Añadir el estado alcanzable al conjunto
                print(f"    Estado {id(state)} tiene transición con '{symbol}' a Estado {id(next_state)}")
        else:
            # Si no hay transiciones con el símbolo, indicar que no se puede mover
            print(f"    Estado {id(state)} no tiene transiciones para el símbolo '{symbol}'")

    # Imprimir los estados alcanzables
    print(f"  Movimiento con símbolo '{symbol}': a estados: {[str(id(state)) for state in next_states]}")
    return next_states  # Retornar el conjunto de estados alcanzables con el símbolo

def simulate_afn(afn, string):
    # Obtener la clausura epsilon del estado inicial del AFN
    current_states = epsilon_closure([afn.start_state])
    print(f"  AFN Estado inicial: {[str(id(state)) for state in current_states]}")

    # Procesar cada símbolo en la cadena de entrada
    for char in string:
        print(f"  Procesando símbolo: '{char}'")
        
        # Obtener los estados alcanzables con el símbolo actual usando la función move
        next_states = move(current_states, char)
        
        # Calcular la clausura epsilon de los estados resultantes después del movimiento
        current_states = epsilon_closure(next_states)
        print(f"  Clausura epsilon después de mover: {[str(id(state)) for state in current_states]}")

        # Si no hay estados alcanzables, terminar la simulación y retornar False
        if not current_states:
            print(f"  No hay estados alcanzables después de procesar '{char}', terminando simulación.")
            return False

    # Verificar si alguno de los estados actuales es un estado de aceptación
    result = any(state.is_accept for state in current_states)
    print(f"  Resultado de simulación AFN: {'Sí' if result else 'No'}")
    return result  # Retornar True si hay al menos un estado de aceptación, False en caso contrario
