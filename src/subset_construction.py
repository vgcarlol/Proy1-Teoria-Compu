class AFD:
    def __init__(self):
        self.states = []
        self.transitions = {}
        self.initial_state = None 
        self.accept_states = []  

def epsilon_closure(states):
    stack = list(states)
    closure = set(states)  

    while stack:
        state = stack.pop()
        for next_state in state.epsilon_transitions:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    
    return closure

def move(states, symbol):
    next_states = set() 
    for state in states:
        if symbol in state.transitions:
            next_states.update(state.transitions[symbol])
    return next_states

def construct_afd(afn):
    initial_closure = epsilon_closure([afn.start_state])
    unmarked_states = [initial_closure]
    state_map = {frozenset(initial_closure): 'S0'}
    afd = AFD()
    afd.transitions = {}
    afd.states = ['S0'] 
    afd.initial_state = 'S0'
    afd.accept_states = []

    if any(state.is_accept for state in initial_closure):
        afd.accept_states.append('S0')

    print(f"  Estado inicial del AFD: 'S0' -> Clausura epsilon: {[str(id(state)) for state in initial_closure]}")

    while unmarked_states:
        current_closure = unmarked_states.pop(0)
        current_state_name = state_map[frozenset(current_closure)]

        symbols = set()
        for state in current_closure:
            symbols.update(state.transitions.keys())

        for symbol in symbols:
            new_closure = epsilon_closure(move(current_closure, symbol))
            print(f"  Procesando símbolo '{symbol}' -> Nueva clausura: {[str(id(state)) for state in new_closure]}")

            if not new_closure:
                continue
            if frozenset(new_closure) not in state_map:
                new_state_name = f'S{len(state_map)}'
                state_map[frozenset(new_closure)] = new_state_name
                afd.states.append(new_state_name)
                unmarked_states.append(new_closure)

                if any(state.is_accept for state in new_closure):
                    afd.accept_states.append(new_state_name)

                print(f"  Nuevo estado del AFD: '{new_state_name}' -> Clausura epsilon: {[str(id(state)) for state in new_closure]}")
            else:
                new_state_name = state_map[frozenset(new_closure)]

            afd.transitions[(current_state_name, symbol)] = new_state_name
            print(f"  Añadida transición AFD: '{current_state_name}' --'{symbol}'--> '{new_state_name}'")

    print(f"  Estados de aceptación del AFD: {afd.accept_states}")
    return afd
