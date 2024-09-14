import os
import graphviz

# Establecer la ruta de Graphviz local
os.environ["PATH"] += os.pathsep + os.path.abspath("./Graphviz/bin")

import os
import graphviz

# Establecer la ruta de Graphviz local
os.environ["PATH"] += os.pathsep + os.path.abspath("./Graphviz/bin")

def generate_afn_graph(afn, file_path):
    try:
        graph = graphviz.Digraph(format='png')
        visited_states = set()  # Conjunto para rastrear los estados ya procesados
        states_to_visit = [afn.start_state]

        # Agregar los estados al grafo
        while states_to_visit:
            state = states_to_visit.pop()
            state_id = str(id(state))

            if state_id in visited_states:
                continue  # Saltar si ya se ha visitado este estado

            visited_states.add(state_id)

            # Marcar estado de aceptación
            if state.is_accept:
                graph.node(state_id, shape='doublecircle')
            else:
                graph.node(state_id, shape='circle')

            # Agregar transiciones normales
            for symbol, next_states in state.transitions.items():
                for next_state in next_states:
                    next_state_id = str(id(next_state))
                    graph.edge(state_id, next_state_id, label=symbol)

                    if next_state_id not in visited_states:
                        states_to_visit.append(next_state)

            # Agregar transiciones epsilon
            for next_state in state.epsilon_transitions:
                next_state_id = str(id(next_state))
                graph.edge(state_id, next_state_id, label='ε')

                if next_state_id not in visited_states:
                    states_to_visit.append(next_state)

        # Renderizar y guardar la imagen
        graph.render(file_path, cleanup=True)
        print(f"  Imagen del AFN generada y guardada como '{file_path}'.")

    except Exception as e:
        print(f"  Error al generar la imagen del AFN: {e}")


def generate_afd_graph(afd, file_path):
    try:
        graph = graphviz.Digraph(format='png')

        # Agregar los estados al grafo
        for state in afd.states:
            shape = 'doublecircle' if state in afd.accept_states else 'circle'
            graph.node(state, shape=shape)

        # Agregar transiciones
        for (state, symbol), next_state in afd.transitions.items():
            graph.edge(state, next_state, label=symbol)

        # Renderizar y guardar la imagen
        graph.render(file_path, cleanup=True)
        print(f"  Imagen del AFD generada y guardada como '{file_path}'.")

    except Exception as e:
        print(f"  Error al generar la imagen del AFD: {e}")
