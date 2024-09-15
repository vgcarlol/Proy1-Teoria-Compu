# Clase que representa un estado en un AFN
class State:
    def __init__(self):
        # Diccionario de transiciones normales: {símbolo: [lista de estados destino]}
        self.transitions = {}
        # Conjunto de transiciones epsilon (ε)
        self.epsilon_transitions = set()
        # Indicador de si el estado es un estado de aceptación
        self.is_accept = False

    def add_transition(self, symbol, state):
        # Añadir una transición normal para un símbolo específico a un estado dado
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)
        # Depuración: mostrar la transición añadida
        print(f"  Añadida transición: {symbol} -> Estado({id(state)})")

    def add_epsilon_transition(self, state):
        # Añadir una transición epsilon (ε) al estado dado
        self.epsilon_transitions.add(state)
        # Depuración: mostrar la transición epsilon añadida
        print(f"  Añadida transición epsilon -> Estado({id(state)})")

# Clase que representa un AFN con un estado inicial y un estado de aceptación
class AFN:
    def __init__(self, start_state, accept_state):
        self.start_state = start_state  # Estado inicial del AFN
        self.accept_state = accept_state  # Estado de aceptación del AFN

# Función que construye un AFN a partir de una expresión regular en notación postfix utilizando el algoritmo de Thompson
def construct_afn(postfix_expression):
    # Pila para almacenar AFNs parciales durante la construcción
    stack = []

    # Procesar cada carácter en la expresión postfix
    for char in postfix_expression:
        if char.isalnum() or char == 'ε':  # Símbolo básico o epsilon
            # Crear un AFN básico para el símbolo
            start_state = State()
            accept_state = State()
            start_state.add_transition(char, accept_state)
            afn = AFN(start_state, accept_state)
            stack.append(afn)
            # Depuración: mostrar el AFN creado para el símbolo
            print(f"Creado AFN para '{char}': start={start_state}, accept={accept_state}")

        elif char == '|':  # Unión
            # Sacar los dos AFNs del tope de la pila
            afn2 = stack.pop()
            afn1 = stack.pop()
            # Crear nuevos estados de inicio y aceptación para el AFN resultante
            start_state = State()
            accept_state = State()

            # Añadir transiciones epsilon al nuevo estado inicial
            start_state.add_epsilon_transition(afn1.start_state)
            start_state.add_epsilon_transition(afn2.start_state)

            # Añadir transiciones epsilon al nuevo estado de aceptación
            afn1.accept_state.add_epsilon_transition(accept_state)
            afn2.accept_state.add_epsilon_transition(accept_state)

            # Crear el nuevo AFN para la unión
            afn = AFN(start_state, accept_state)
            stack.append(afn)
            # Depuración: mostrar el AFN creado para la unión
            print(f"Creado AFN para '|': start={start_state}, accept={accept_state}")

        elif char == '.':  # Concatenación
            # Sacar los dos AFNs del tope de la pila
            afn2 = stack.pop()
            afn1 = stack.pop()

            # Conectar el estado de aceptación del primer AFN al estado inicial del segundo AFN con una transición epsilon
            afn1.accept_state.add_epsilon_transition(afn2.start_state)
            # El estado intermedio ya no es un estado de aceptación
            afn1.accept_state.is_accept = False

            # Crear el nuevo AFN para la concatenación
            afn = AFN(afn1.start_state, afn2.accept_state)
            stack.append(afn)
            # Depuración: mostrar el AFN creado para la concatenación
            print(f"Creado AFN para '.': start={afn1.start_state}, accept={afn2.accept_state}")

        elif char == '*':  # Estrella de Kleene
            # Sacar el AFN del tope de la pila
            afn1 = stack.pop()
            # Crear nuevos estados de inicio y aceptación para el AFN resultante
            start_state = State()
            accept_state = State()

            # Añadir transiciones epsilon para la estrella de Kleene
            start_state.add_epsilon_transition(afn1.start_state)
            start_state.add_epsilon_transition(accept_state)
            afn1.accept_state.add_epsilon_transition(afn1.start_state)
            afn1.accept_state.add_epsilon_transition(accept_state)
            # El estado anterior ya no es un estado de aceptación
            afn1.accept_state.is_accept = False

            # Crear el nuevo AFN para la estrella de Kleene
            afn = AFN(start_state, accept_state)
            stack.append(afn)
            # Depuración: mostrar el AFN creado para la estrella de Kleene
            print(f"Creado AFN para '*': start={start_state}, accept={accept_state}")

    # Extraer el AFN final de la pila
    final_afn = stack.pop()
    # Marcar el estado de aceptación del AFN final como estado de aceptación
    final_afn.accept_state.is_accept = True
    # Depuración: mostrar el AFN final creado
    print(f"AFN final: start={final_afn.start_state}, accept={final_afn.accept_state}")

    # Depuración: Listar todas las transiciones finales del AFN
    visited_states = set()
    states_to_visit = [final_afn.start_state]

    print("\n--- Estados y transiciones finales del AFN ---")
    while states_to_visit:
        state = states_to_visit.pop()
        state_id = id(state)
        if state_id in visited_states:
            continue
        visited_states.add(state_id)

        # Mostrar las transiciones del estado actual
        print(f"Estado {state_id}: Transiciones {state.transitions}, Epsilon {[id(s) for s in state.epsilon_transitions]}")
        
        # Añadir los estados siguientes a la lista para visitar
        for symbol, next_states in state.transitions.items():
            states_to_visit.extend(next_states)
        states_to_visit.extend(state.epsilon_transitions)

    # Retornar el AFN final construido
    return final_afn
