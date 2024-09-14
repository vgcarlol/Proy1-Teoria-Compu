def simulate_afd(afd, string):
    current_state = afd.initial_state
    print(f"  AFD Estado inicial: '{current_state}'")

    for char in string:
        print(f"  Procesando símbolo: '{char}'")
        current_state = afd.transitions.get((current_state, char))
        if current_state is None:
            print(f"  No hay transición para el símbolo: '{char}', estado actual: 'None'")
            return False
        print(f"  Estado actual: '{current_state}'")

    result = current_state in afd.accept_states
    print(f"  Resultado de simulación AFD: {'Sí' if result else 'No'}")
    return result
