def epsilon_closure(states):
    stack = list(states)
    closure = set(states)
    print(f"  Calculando clausura epsilon para estados: {[str(id(state)) for state in states]}")

    while stack:
        state = stack.pop()
        for next_state in state.epsilon_transitions:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
                print(f"    Añadiendo estado {id(next_state)} a la clausura epsilon")

    print(f"  Clausura epsilon resultante: {[str(id(state)) for state in closure]}")
    return closure

def move(states, symbol):
    next_states = set()
    print(f"  Intentando mover con símbolo '{symbol}' desde los estados: {[str(id(state)) for state in states]}")
    
    for state in states:
        if symbol in state.transitions:
            for next_state in state.transitions[symbol]:
                next_states.add(next_state)
                print(f"    Estado {id(state)} tiene transición con '{symbol}' a Estado {id(next_state)}")
        else:
            print(f"    Estado {id(state)} no tiene transiciones para el símbolo '{symbol}'")

    print(f"  Movimiento con símbolo '{symbol}': a estados: {[str(id(state)) for state in next_states]}")
    return next_states

def simulate_afn(afn, string):
    current_states = epsilon_closure([afn.start_state])
    print(f"  AFN Estado inicial: {[str(id(state)) for state in current_states]}")

    for char in string:
        print(f"  Procesando símbolo: '{char}'")

        next_states = move(current_states, char)

        current_states = epsilon_closure(next_states)
        print(f"  Clausura epsilon después de mover: {[str(id(state)) for state in current_states]}")

        if not current_states:
            print(f"  No hay estados alcanzables después de procesar '{char}', terminando simulación.")
            return False

    result = any(state.is_accept for state in current_states)
    print(f"  Resultado de simulación AFN: {'Sí' if result else 'No'}")
    return result
