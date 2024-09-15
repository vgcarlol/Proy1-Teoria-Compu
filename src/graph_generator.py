import os
import graphviz

# Establecer la ruta de Graphviz local para asegurarse de que el ejecutable 'dot' se pueda encontrar
os.environ["PATH"] += os.pathsep + os.path.abspath("./Graphviz/bin")

def generate_afn_graph(afn, file_path):
    try:
        # Crear un nuevo grafo dirigido utilizando Graphviz con formato de salida PNG
        graph = graphviz.Digraph(format='png')
        visited_states = set()  # Conjunto para rastrear los estados ya procesados
        states_to_visit = [afn.start_state]  # Comenzar con el estado inicial del AFN

        # Agregar los estados al grafo
        while states_to_visit:
            state = states_to_visit.pop()  # Obtener el estado actual
            state_id = str(id(state))  # Identificador único del estado (ID de objeto)

            # Si el estado ya fue procesado, saltarlo
            if state_id in visited_states:
                continue

            # Marcar el estado como visitado
            visited_states.add(state_id)

            # Marcar estado de aceptación
            if state.is_accept:
                # Si es un estado de aceptación, usar doble círculo para el nodo
                graph.node(state_id, shape='doublecircle')
            else:
                # Si no es un estado de aceptación, usar círculo simple
                graph.node(state_id, shape='circle')

            # Agregar transiciones normales
            for symbol, next_states in state.transitions.items():
                for next_state in next_states:
                    next_state_id = str(id(next_state))  # ID único del estado de destino
                    graph.edge(state_id, next_state_id, label=symbol)  # Crear una arista etiquetada con el símbolo

                    # Agregar el siguiente estado a la lista si no ha sido visitado
                    if next_state_id not in visited_states:
                        states_to_visit.append(next_state)

            # Agregar transiciones epsilon
            for next_state in state.epsilon_transitions:
                next_state_id = str(id(next_state))  # ID único del estado de destino
                graph.edge(state_id, next_state_id, label='ε')  # Crear una arista etiquetada con epsilon (ε)

                # Agregar el siguiente estado a la lista si no ha sido visitado
                if next_state_id not in visited_states:
                    states_to_visit.append(next_state)

        # Renderizar y guardar la imagen en el archivo especificado
        graph.render(file_path, cleanup=True)
        print(f"  Imagen del AFN generada y guardada como '{file_path}'.")

    except Exception as e:
        # Manejar y mostrar cualquier error que ocurra durante la generación de la imagen
        print(f"  Error al generar la imagen del AFN: {e}")

def generate_afd_graph(afd, file_path):
    try:
        # Crear un nuevo grafo dirigido utilizando Graphviz con formato de salida PNG
        graph = graphviz.Digraph(format='png')

        # Agregar los estados al grafo
        for state in afd.states:
            # Determinar la forma del nodo: 'doublecircle' para los estados de aceptación, 'circle' para los demás
            shape = 'doublecircle' if state in afd.accept_states else 'circle'
            graph.node(state, shape=shape)  # Agregar el nodo al grafo

        # Agregar transiciones
        for (state, symbol), next_state in afd.transitions.items():
            # Crear una arista etiquetada con el símbolo que va del estado actual al siguiente estado
            graph.edge(state, next_state, label=symbol)

        # Renderizar y guardar la imagen en el archivo especificado
        graph.render(file_path, cleanup=True)
        print(f"  Imagen del AFD generada y guardada como '{file_path}'.")

    except Exception as e:
        # Manejar y mostrar cualquier error que ocurra durante la generación de la imagen
        print(f"  Error al generar la imagen del AFD: {e}")
