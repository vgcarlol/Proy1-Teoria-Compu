class State:
    def __init__(self):    
        self.transitions = {}
        self.epsilon_transitions = set()
        self.is_accept = False

    def add_transition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)
        print(f"  Añadida transición: {symbol} -> Estado({id(state)})")

    def add_epsilon_transition(self, state):
        self.epsilon_transitions.add(state)
        print(f"  Añadida transición epsilon -> Estado({id(state)})")
class AFN:
    def __init__(self, start_state, accept_state):
        self.start_state = start_state
        self.accept_state = accept_state

def construct_afn(postfix_expression):
    stack = []

    for char in postfix_expression:
        if char.isalnum() or char == 'ε':
            start_state = State()
            accept_state = State()
            start_state.add_transition(char, accept_state)
            afn = AFN(start_state, accept_state)
            stack.append(afn)
            print(f"Creado AFN para '{char}': start={start_state}, accept={accept_state}")

        elif char == '|':
            afn2 = stack.pop()
            afn1 = stack.pop()
            start_state = State()
            accept_state = State()

            start_state.add_epsilon_transition(afn1.start_state)
            start_state.add_epsilon_transition(afn2.start_state)

            afn1.accept_state.add_epsilon_transition(accept_state)
            afn2.accept_state.add_epsilon_transition(accept_state)

            afn = AFN(start_state, accept_state)
            stack.append(afn)
            print(f"Creado AFN para '|': start={start_state}, accept={accept_state}")

        elif char == '.':
            afn2 = stack.pop()
            afn1 = stack.pop()
            afn1.accept_state.add_epsilon_transition(afn2.start_state)
            afn1.accept_state.is_accept = False

            afn = AFN(afn1.start_state, afn2.accept_state)
            stack.append(afn)
            print(f"Creado AFN para '.': start={afn1.start_state}, accept={afn2.accept_state}")

        elif char == '*':
            afn1 = stack.pop()
            start_state = State()
            accept_state = State()

            start_state.add_epsilon_transition(afn1.start_state)
            start_state.add_epsilon_transition(accept_state)
            afn1.accept_state.add_epsilon_transition(afn1.start_state)
            afn1.accept_state.add_epsilon_transition(accept_state)
            afn1.accept_state.is_accept = False

            afn = AFN(start_state, accept_state)
            stack.append(afn)
            print(f"Creado AFN para '*': start={start_state}, accept={accept_state}")

    final_afn = stack.pop()
    final_afn.accept_state.is_accept = True
    print(f"AFN final: start={final_afn.start_state}, accept={final_afn.accept_state}")

    visited_states = set()
    states_to_visit = [final_afn.start_state]

    print("\n--- Estados y transiciones finales del AFN ---")
    while states_to_visit:
        state = states_to_visit.pop()
        state_id = id(state)
        if state_id in visited_states:
            continue
        visited_states.add(state_id)
        print(f"Estado {state_id}: Transiciones {state.transitions}, Epsilon {[id(s) for s in state.epsilon_transitions]}")

        for symbol, next_states in state.transitions.items():
            states_to_visit.extend(next_states)
        states_to_visit.extend(state.epsilon_transitions)
    return final_afn
