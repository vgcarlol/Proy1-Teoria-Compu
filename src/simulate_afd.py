def simulate_afd(afd, string):
    # Inicializar el estado actual con el estado inicial del AFD
    current_state = afd.initial_state
    print(f"  AFD Estado inicial: '{current_state}'")

    # Recorrer cada símbolo en la cadena de entrada
    for char in string:
        print(f"  Procesando símbolo: '{char}'")  # Imprimir el símbolo que se está procesando
        # Intentar encontrar la transición en el AFD para el estado actual y el símbolo
        current_state = afd.transitions.get((current_state, char))
        
        # Si no hay una transición definida, la cadena no es aceptada por el AFD
        if current_state is None:
            print(f"  No hay transición para el símbolo: '{char}', estado actual: 'None'")
            return False  # Retornar False ya que la cadena no puede ser procesada correctamente
        
        # Imprimir el nuevo estado al que se ha movido el AFD
        print(f"  Estado actual: '{current_state}'")

    # Verificar si el estado final después de procesar toda la cadena es un estado de aceptación
    result = current_state in afd.accept_states
    print(f"  Resultado de simulación AFD: {'Sí' if result else 'No'}")  # Imprimir el resultado final
    return result  # Retornar True si es un estado de aceptación, False en caso contrario
