from subset_construction import AFD


def minimize_afd(afd):
    partitions = [set(afd.accept_states), set(state for state in afd.states if state not in afd.accept_states)]
    new_partitions = []

    while True:
        for partition in partitions:
            subsets = {}
            for state in partition:
                signature = tuple((symbol, afd.transitions.get((state, symbol))) for symbol in afd.transitions)
                if signature in subsets:
                    subsets[signature].add(state)
                else:
                    subsets[signature] = {state}

            new_partitions.extend(subsets.values())

        if new_partitions == partitions:
            break
        partitions = new_partitions
        new_partitions = []

    # Generar el AFD minimizado a partir de las particiones
    minimized_afd = AFD()
    state_map = {}
    for i, partition in enumerate(partitions):
        new_state_name = f'M{i}'
        minimized_afd.states.append(new_state_name)
        if afd.initial_state in partition:
            minimized_afd.initial_state = new_state_name
        if partition.intersection(afd.accept_states):
            minimized_afd.accept_states.append(new_state_name)
        for state in partition:
            state_map[state] = new_state_name

    for (state, symbol), target in afd.transitions.items():
        if state in state_map and target in state_map:
            minimized_afd.transitions[(state_map[state], symbol)] = state_map[target]

    return minimized_afd
