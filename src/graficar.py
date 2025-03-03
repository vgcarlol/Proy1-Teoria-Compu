import os
import sys
import logging
from graphviz import Digraph
from regex_functions import shuntingYard  # Importar función de regex para conversión a postfix
from utilidades import Stack, Node  # Importar clases Stack y Node desde utilidades.py

# Configurar Graphviz para ejecutarse desde la carpeta raíz del repositorio
GRAPHVIZ_PATH = os.path.abspath("./Graphviz/bin")

# Agregar la ruta de Graphviz al PATH del sistema
os.environ["PATH"] += os.pathsep + GRAPHVIZ_PATH

# Verificar que Graphviz esté correctamente instalado
if not os.path.exists(GRAPHVIZ_PATH):
    raise EnvironmentError(f"⚠️ Error: La carpeta '{GRAPHVIZ_PATH}' no existe. Asegúrate de que Graphviz esté instalado en la ubicación correcta.")

dot_executable = os.path.join(GRAPHVIZ_PATH, "dot")
if not os.path.exists(dot_executable) and not os.path.exists(dot_executable + ".exe"):
    raise EnvironmentError(f"⚠️ Error: No se encontró 'dot' en '{GRAPHVIZ_PATH}'. Verifica que Graphviz esté instalado correctamente.")

# Configuración de logging para depuración
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Crear la carpeta 'output' si no existe
def asegurar_directorio(directorio):
    if not os.path.exists(directorio):
        os.makedirs(directorio)

# Función para graficar un Autómata Finito No Determinista (AFN)
def graficarAFN(afn, i):
    directorio_afn = "output/afn"
    asegurar_directorio(directorio_afn)

    node = Digraph()
    node.attr(rankdir='LR')

    # Agregar nodos
    for state in range(afn.accept + 1):
        shape = "doublecircle" if state == afn.accept else "circle"
        node.node(str(state), shape=shape)
    
    # Agregar transiciones
    for (state, symbol), next_states in afn.transitions.items():
        for next_state in next_states:
            node.edge(str(state), str(next_state), label=symbol if symbol else 'ε')
    
    # Guardar y renderizar el archivo
    node.render(f'{directorio_afn}/afn_{i}.gv', view=False, format='jpg')

# Función para graficar un Autómata Finito Determinista (AFD)
def graficarAFD(afd, i, simplified=False):
    if simplified:
        directorio_afd = "output/afdminimization"
        asegurar_directorio(directorio_afd)
        dot = afd.visualize()
        dot.render(f'{directorio_afd}/afdmin_{i}.gv', view=False, format='jpg')
    else:
        directorio_afd = "output/afd"
        asegurar_directorio(directorio_afd)
        dot = afd.visualize()
        dot.render(f'{directorio_afd}/afd_{i}.gv', view=False, format='jpg')

# Clase para representar y graficar un Árbol de Expresión Regular
class Tree:
    def __init__(self, root, name):
        self.root = root
        self.name = name
    
    def graficar(self):
        directorio_ast = "output"
        asegurar_directorio(directorio_ast)

        graph = Digraph('G', filename=f'{directorio_ast}/AST-{self.name}.gv', format='jpg')
        self.root.graficarNodo(graph)
        graph.view()

# Función para graficar el Árbol de una Expresión Regular
def graficarArbol(regex):
    for i, expresion in enumerate(regex):
        logging.info(f"Arbol de la expresión regular: {expresion}")
        postfix = shuntingYard(expresion)
        logging.info(f"Postfix: {postfix}")
        tree = Tree(createTree(postfix), i)
        tree.graficar()

# Función para construir el Árbol de la Expresión Regular
def createTree(regex):
    stack = Stack()
    operators = ['*', '|', '.']

    for i, symbol in enumerate(regex):
        if symbol in operators:
            if symbol == '|':
                right, left = stack.pop(), stack.pop()
                node = Node(symbol, f'{i}', left, right)
                stack.push(node)
            elif symbol == '.':
                right, left = stack.pop(), stack.pop()
                node = Node(symbol, f'{i}', left, right)
                stack.push(node)
            elif symbol == '*':
                left = stack.pop()
                node = Node(symbol, f'{i}', left)
                stack.push(node)
        else:
            node = Node(symbol, f'{i}')
            stack.push(node)

    return stack.pop()
