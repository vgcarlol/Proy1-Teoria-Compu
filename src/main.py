import os
from shunting_yard import infix_to_postfix
from thompson import construct_afn
from subset_construction import construct_afd
from minimization import minimize_afd
from simulate_afn import simulate_afn
from simulate_afd import simulate_afd
from graph_generator import generate_afn_graph, generate_afd_graph
from file_reader import read_input

def create_output_dirs():
    # Crear directorios de salida si no existen
    os.makedirs('output/afn_graphs', exist_ok=True)
    os.makedirs('output/afd_graphs', exist_ok=True)
    os.makedirs('output/afd_minimized_graphs', exist_ok=True)

def print_afn_transitions(afn):
    visited_states = set()
    states_to_visit = [afn.start_state]

    print("\n--- Estados y transiciones del AFN ---")
    while states_to_visit:
        state = states_to_visit.pop()
        state_id = id(state)
        if state_id in visited_states:
            continue
        visited_states.add(state_id)

        print(f"Estado {state_id}:")
        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                print(f"  Transición: '{symbol}' -> Estado {id(next_state)}")
                states_to_visit.append(next_state)
        for epsilon_state in state.epsilon_transitions:
            print(f"  Epsilon -> Estado {id(epsilon_state)}")
            states_to_visit.append(epsilon_state)

def print_afd_transitions(afd):
    print("\n--- Estados y transiciones del AFD ---")
    for (state, symbol), next_state in afd.transitions.items():
        print(f"Estado '{state}' --'{symbol}'--> '{next_state}'")
    print(f"Estados de aceptación: {afd.accept_states}")

def main():
    # Crear directorios de salida
    create_output_dirs()
    
    # Leer las expresiones regulares y cadenas desde un archivo
    expressions = read_input('input/expressions.txt')

    for idx, (regex, string) in enumerate(expressions):
        print(f"\n[Expresión {idx + 1}/{len(expressions)}] Procesando: {regex} con la cadena: {string}")
        
        try:
            # 1. Convertir expresión regular infix a postfix
            postfix = infix_to_postfix(regex)
            print(f"  Postfix: {postfix}")
            
            # 2. Construir el AFN utilizando el algoritmo de Thompson
            afn = construct_afn(postfix)
            print(f"  AFN construido. Generando imagen...")
            generate_afn_graph(afn, f'output/afn_graphs/{idx}_afn.png')

            # Depurar transiciones del AFN
            print_afn_transitions(afn)

            # 3. Convertir el AFN a AFD
            afd = construct_afd(afn)
            print(f"  AFD construido. Generando imagen...")
            generate_afd_graph(afd, f'output/afd_graphs/{idx}_afd.png')

            # Depurar transiciones del AFD
            print_afd_transitions(afd)

            # 4. Minimizar el AFD
            minimized_afd = minimize_afd(afd)
            print(f"  AFD minimizado. Generando imagen...")
            generate_afd_graph(minimized_afd, f'output/afd_minimized_graphs/{idx}_afd_minimized.png')

            # 5. Limpiar y manejar la cadena vacía para simulación
            string = string.strip()
            if string in ['ε', 'Îµ']:  # Cualquier interpretación de 'ε'
                string = ''  # Interpretar 'ε' como cadena vacía
            print(f"  Simulando AFN con la cadena: '{string}'")
            afn_result = simulate_afn(afn, string)
            print(f"  Simulando AFD minimizado con la cadena: '{string}'")
            afd_result = simulate_afd(minimized_afd, string)

            # 6. Mostrar los resultados
            print(f"  Resultado AFN: {'Sí' if afn_result else 'No'}")
            print(f"  Resultado AFD minimizado: {'Sí' if afd_result else 'No'}\n")

        except Exception as e:
            print(f"  Error al procesar la expresión regular '{regex}': {e}\n")

if __name__ == '__main__':
    main()
