import os
# Importar funciones de otros módulos para las diferentes etapas de la construcción y simulación de autómatas
from shunting_yard import infix_to_postfix  # Convierte expresiones regulares de infix a postfix
from thompson import construct_afn  # Construye el AFN usando el algoritmo de Thompson
from subset_construction import construct_afd  # Convierte el AFN a AFD utilizando el algoritmo de subconjuntos
from minimization import minimize_afd  # Minimiza el AFD
from simulate_afn import simulate_afn  # Simula si una cadena es aceptada por un AFN
from simulate_afd import simulate_afd  # Simula si una cadena es aceptada por un AFD
from graph_generator import generate_afn_graph, generate_afd_graph  # Genera gráficos visuales del AFN y AFD
from file_reader import read_input  # Lee las expresiones regulares y cadenas desde un archivo de texto

def create_output_dirs():
    # Crear directorios de salida si no existen. Estos directorios almacenarán las imágenes de los autómatas generados.
    os.makedirs('output/afn_graphs', exist_ok=True)
    os.makedirs('output/afd_graphs', exist_ok=True)
    os.makedirs('output/afd_minimized_graphs', exist_ok=True)

def print_afn_transitions(afn):
    # Esta función imprime las transiciones del AFN generado, mostrando las conexiones entre los estados
    visited_states = set()  # Conjunto para rastrear estados visitados
    states_to_visit = [afn.start_state]  # Comenzar con el estado inicial del AFN

    print("\n--- Estados y transiciones del AFN ---")
    while states_to_visit:
        state = states_to_visit.pop()  # Tomar un estado para procesar sus transiciones
        state_id = id(state)  # Usar la ID única del estado para identificarlo
        if state_id in visited_states:
            continue  # Saltar si el estado ya ha sido visitado
        visited_states.add(state_id)  # Marcar el estado como visitado

        print(f"Estado {state_id}:")
        # Imprimir transiciones normales
        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                print(f"  Transición: '{symbol}' -> Estado {id(next_state)}")
                states_to_visit.append(next_state)  # Agregar el siguiente estado a la lista para procesarlo
        # Imprimir transiciones epsilon
        for epsilon_state in state.epsilon_transitions:
            print(f"  Epsilon -> Estado {id(epsilon_state)}")
            states_to_visit.append(epsilon_state)

def print_afd_transitions(afd):
    # Esta función imprime las transiciones del AFD generado
    print("\n--- Estados y transiciones del AFD ---")
    for (state, symbol), next_state in afd.transitions.items():
        print(f"Estado '{state}' --'{symbol}'--> '{next_state}'")
    print(f"Estados de aceptación: {afd.accept_states}")

def main():
    # Crear los directorios necesarios para almacenar las imágenes de los autómatas
    create_output_dirs()
    
    # Leer las expresiones regulares y cadenas desde un archivo
    expressions = read_input('input/expressions.txt')

    # Procesar cada expresión regular y cadena en el archivo de entrada
    for idx, (regex, string) in enumerate(expressions):
        print(f"\n[Expresión {idx + 1}/{len(expressions)}] Procesando: {regex} con la cadena: {string}")
        
        try:
            # 1. Shunting Yard para transformar de infix a postfix
            print("---- Shunting Yard: Transformar de infix a postfix ----")
            postfix = infix_to_postfix(regex)  # Convertir la expresión infix a postfix
            print(f"  Postfix: {postfix}")
            
            # 2. Generación de AFN con Thompson
            print("---- Generación de AFN con Thompson ----")
            afn = construct_afn(postfix)  # Construir el AFN usando el algoritmo de Thompson
            print(f"  AFN construido. Generando imagen...")
            generate_afn_graph(afn, f'output/afn_graphs/{idx}_afn.png')  # Generar y guardar la imagen del AFN

            # Depurar transiciones del AFN
            print_afn_transitions(afn)  # Imprimir las transiciones del AFN

            # 3. Generación de AFD con subconjuntos
            print("---- Generación de AFD con Subconjuntos ----")
            afd = construct_afd(afn)  # Convertir el AFN a AFD
            print(f"  AFD construido. Generando imagen...")
            generate_afd_graph(afd, f'output/afd_graphs/{idx}_afd.png')  # Generar y guardar la imagen del AFD

            # Depurar transiciones del AFD
            print_afd_transitions(afd)  # Imprimir las transiciones del AFD

            # 4. Minimización de AFD
            print("---- Minimización de AFD ----")
            minimized_afd = minimize_afd(afd)  # Minimizar el AFD
            print(f"  AFD minimizado. Generando imagen...")
            generate_afd_graph(minimized_afd, f'output/afd_minimized_graphs/{idx}_afd_minimized.png')  # Guardar la imagen del AFD minimizado

            # 5. Simulación de AFN y AFD
            print("---- Simulación de AFN y AFDs ----")
            # Limpiar y manejar la cadena vacía para simulación
            string = string.strip()
            if string in ['ε', 'Îµ']:  # Manejar diferentes representaciones del símbolo epsilon
                string = ''  # Interpretar 'ε' como cadena vacía
            print(f"  Simulando AFN con la cadena: '{string}'")
            afn_result = simulate_afn(afn, string)  # Simular la cadena con el AFN
            print(f"  Simulando AFD minimizado con la cadena: '{string}'")
            afd_result = simulate_afd(minimized_afd, string)  # Simular la cadena con el AFD minimizado

            # 6. Mostrar los resultados
            print(f"  Resultado AFN: {'Sí' if afn_result else 'No'}")
            print(f"  Resultado AFD minimizado: {'Sí' if afd_result else 'No'}\n")

        except Exception as e:
            # Capturar y mostrar cualquier error que ocurra durante el proceso
            print(f"  Error al procesar la expresión regular '{regex}': {e}\n")

# Punto de entrada del programa
if __name__ == '__main__':
    main()
