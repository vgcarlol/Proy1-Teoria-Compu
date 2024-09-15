# Clase que representa un AFD (Autómata Finito Determinista)
class AFD:
    def __init__(self):
        self.states = []  # Lista de estados en el AFD
        self.transitions = {}  # Diccionario de transiciones en el formato {(estado, símbolo): estado_destino}
        self.initial_state = None  # Estado inicial del AFD
        self.accept_states = []  # Lista de estados de aceptación

# Función para calcular la clausura epsilon para un conjunto de estados
def epsilon_closure(states):
    stack = list(states)  # Convertir los estados de entrada en una pila
    closure = set(states)  # Inicializar la clausura epsilon con los estados de entrada
    
    # Bucle para procesar todos los estados en la pila
    while stack:
        state = stack.pop()  # Extraer un estado de la pila
        # Recorrer las transiciones epsilon del estado actual
        for next_state in state.epsilon_transitions:
            # Si el estado alcanzable no está en la clausura, añadirlo
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)  # Añadir el nuevo estado a la pila para procesar sus transiciones epsilon
    
    return closure  # Retornar el conjunto de estados que forman la clausura epsilon

# Función para calcular el conjunto de estados alcanzables desde un conjunto de estados dado un símbolo específico
def move(states, symbol):
    next_states = set()  # Inicializar un conjunto para los estados alcanzables
    for state in states:
        # Verificar si el estado tiene transiciones definidas para el símbolo
        if symbol in state.transitions:
            # Añadir todos los estados resultantes de las transiciones para 'symbol'
            next_states.update(state.transitions[symbol])
    return next_states  # Retornar el conjunto de estados alcanzables

# Función para construir un AFD a partir de un AFN usando el método de construcción de subconjuntos
def construct_afd(afn):
    # Inicializar la construcción del AFD
    initial_closure = epsilon_closure([afn.start_state])  # Obtener la clausura epsilon del estado inicial del AFN
    unmarked_states = [initial_closure]  # Lista de estados no procesados (subconjuntos)
    state_map = {frozenset(initial_closure): 'S0'}  # Mapa para asignar nombres a los estados del AFD
    afd = AFD()  # Crear una instancia del AFD
    afd.transitions = {}
    afd.states = ['S0']  # El primer estado del AFD se llama 'S0'
    afd.initial_state = 'S0'
    afd.accept_states = []  # Lista para almacenar los estados de aceptación del AFD

    # Verificar si el estado inicial del AFD es un estado de aceptación
    if any(state.is_accept for state in initial_closure):
        afd.accept_states.append('S0')  # Si alguno de los estados en la clausura es de aceptación, añadir 'S0' a los estados de aceptación

    print(f"  Estado inicial del AFD: 'S0' -> Clausura epsilon: {[str(id(state)) for state in initial_closure]}")

    # Bucle principal para procesar los subconjuntos (estados del AFD)
    while unmarked_states:
        current_closure = unmarked_states.pop(0)  # Obtener el siguiente subconjunto de estados
        current_state_name = state_map[frozenset(current_closure)]  # Obtener el nombre del estado correspondiente en el AFD

        # Encontrar todos los símbolos posibles a partir del estado actual
        symbols = set()
        for state in current_closure:
            symbols.update(state.transitions.keys())  # Recopilar todos los símbolos que tienen transiciones

        # Procesar cada símbolo
        for symbol in symbols:
            # Calcular el nuevo conjunto de estados alcanzables y su clausura epsilon
            new_closure = epsilon_closure(move(current_closure, symbol))
            print(f"  Procesando símbolo '{symbol}' -> Nueva clausura: {[str(id(state)) for state in new_closure]}")

            # Si el conjunto de estados resultante está vacío, no hay transición que agregar
            if not new_closure:
                continue

            # Si el nuevo conjunto de estados no está en el mapa, se crea un nuevo estado en el AFD
            if frozenset(new_closure) not in state_map:
                new_state_name = f'S{len(state_map)}'  # Nombrar el nuevo estado como 'S' seguido del número total de estados
                state_map[frozenset(new_closure)] = new_state_name  # Mapear el nuevo conjunto de estados a su nombre
                afd.states.append(new_state_name)  # Añadir el nuevo estado a la lista de estados del AFD
                unmarked_states.append(new_closure)  # Añadir el nuevo conjunto de estados a la lista de no procesados

                # Verificar si el nuevo estado contiene algún estado de aceptación del AFN
                if any(state.is_accept for state in new_closure):
                    afd.accept_states.append(new_state_name)  # Si es así, añadirlo a la lista de estados de aceptación

                print(f"  Nuevo estado del AFD: '{new_state_name}' -> Clausura epsilon: {[str(id(state)) for state in new_closure]}")
            else:
                # Si el conjunto de estados ya está en el mapa, obtener su nombre
                new_state_name = state_map[frozenset(new_closure)]

            # Añadir la transición al AFD
            afd.transitions[(current_state_name, symbol)] = new_state_name
            print(f"  Añadida transición AFD: '{current_state_name}' --'{symbol}'--> '{new_state_name}'")

    print(f"  Estados de aceptación del AFD: {afd.accept_states}")
    return afd  # Retornar el AFD construido
