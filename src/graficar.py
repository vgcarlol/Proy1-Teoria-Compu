from graphviz import Digraph
from regex_functions import infixToPostfix  # Importar función de regex para conversión a postfix
from utilidades import Stack, Node  # Importar clases Stack y Node desde utilidades.py
import os

# Crear la carpeta 'output' si no existe
if not os.path.exists('output'):
    os.makedirs('output')


def graficarAFN(afn, i):
    node = Digraph()
    node.attr(rankdir='LR')
    for state in range(afn.accept + 1):
        if state == afn.accept:
            node.node(str(state), shape='doublecircle')
        else:
            node.node(str(state))
    for (state, symbol), next_states in afn.transitions.items():
        for next_state in next_states:
            node.edge(str(state), str(next_state), label=symbol if symbol else 'ε')
    node.render(f'output/afn_{i}.gv', view=False, format='jpg')


def graficarAFD(afd, i, simplified = False):
    if simplified:
        dot = afd.visualize()
        dot.render(f'output/afdsimple_{i}.gv', view=False, format='jpg')

    else:
        dot = afd.visualize()
        dot.render(f'output/afd_{i}.gv', view=False, format='jpg')

class Tree:
    def __init__(self, root, name):
        self.root = root
        self.name = name
    
    def graficar(self):
        graph = Digraph('G', filename=f'output/AST-{self.name}.gv', format='jpg')
        self.root.graficarNodo(graph)
        graph.view()

def graficarArbol(regex):
    for i in range(len(regex)):

        print("Arbol de la expresion regular: ", regex[i])
        postfix = infixToPostfix(regex[i])
        print("Postfix: ", postfix)
        tree = Tree(createTree(postfix),i)
        tree.graficar()

def createTree(regex):
    stack = Stack()
    operators = ['*', '|', '.']
    for i in range(len(regex)):
        if regex[i] in operators:
            if regex[i] == '|':
                right = stack.pop()
                left = stack.pop()
                node = Node(regex[i], f'{i}')
                node.left = left
                node.right = right
                stack.push(node)
            elif regex[i] == '.':
                right = stack.pop()
                left = stack.pop()
                node = Node(regex[i], f'{i}')
                node.left = left
                node.right = right
                stack.push(node)
            elif regex[i] == '*':
                left = stack.pop()
                node = Node(regex[i], f'{i}')
                node.left = left
                stack.push(node)
        else:
            node = Node(regex[i], f'{i}')
            stack.push(node)

    return (stack.pop())
