from subset_construction import AFD

def minimize_afd(afd):
    # Inicializar las particiones del AFD:
    # La primera partición contiene los estados de aceptación.
    # La segunda partición contiene los estados que no son de aceptación.
    partitions = [set(afd.accept_states), set(state for state in afd.states if state not in afd.accept_states)]
    new_partitions = []  # Nueva lista para guardar las particiones refinadas.

    # Bucle principal para refinar las particiones hasta que ya no haya cambios.
    while True:
        for partition in partitions:
            subsets = {}  # Diccionario para almacenar subconjuntos según su firma de transición.

            # Crear subconjuntos basados en las transiciones de los estados en la partición actual.
            for state in partition:
                # La "firma" de un estado incluye las transiciones para cada símbolo del AFD.
                signature = tuple((symbol, afd.transitions.get((state, symbol))) for symbol in afd.transitions)

                # Agrupar los estados en subconjuntos según su firma de transición.
                if signature in subsets:
                    subsets[signature].add(state)
                else:
                    subsets[signature] = {state}

            # Agregar los subconjuntos generados a las nuevas particiones.
            new_partitions.extend(subsets.values())

        # Si las nuevas particiones son iguales a las anteriores, se ha alcanzado un punto fijo.
        if new_partitions == partitions:
            break  # Salir del bucle, ya que las particiones no cambian más.

        # Actualizar las particiones y limpiar las nuevas particiones para la siguiente iteración.
        partitions = new_partitions
        new_partitions = []

    # Generar el AFD minimizado a partir de las particiones encontradas.
    minimized_afd = AFD()
    state_map = {}  # Mapa para relacionar los estados originales con los nuevos estados minimizados.

    # Crear nuevos estados para el AFD minimizado basados en las particiones.
    for i, partition in enumerate(partitions):
        new_state_name = f'M{i}'  # Nombrar los nuevos estados como 'M0', 'M1', etc.
        minimized_afd.states.append(new_state_name)

        # Si el estado inicial original está en la partición, asignarlo como el estado inicial del AFD minimizado.
        if afd.initial_state in partition:
            minimized_afd.initial_state = new_state_name

        # Si algún estado de la partición es un estado de aceptación, marcar el nuevo estado como de aceptación.
        if partition.intersection(afd.accept_states):
            minimized_afd.accept_states.append(new_state_name)

        # Asignar los estados originales de la partición al nuevo estado minimizado.
        for state in partition:
            state_map[state] = new_state_name

    # Crear las transiciones del AFD minimizado basadas en las nuevas particiones.
    for (state, symbol), target in afd.transitions.items():
        # Verificar que los estados de origen y destino están en el mapa de estados minimizados.
        if state in state_map and target in state_map:
            # Agregar la transición al AFD minimizado usando los nuevos estados.
            minimized_afd.transitions[(state_map[state], symbol)] = state_map[target]

    # Retornar el AFD minimizado.
    return minimized_afd
