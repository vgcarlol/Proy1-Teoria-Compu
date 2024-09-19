import copy 
import string
from utilidades import conjuntoToString  # Para la conversión de conjuntos a cadenas
from graphviz import Digraph


# Subconjuntos
def formarSubconjunto(conjuntoActual, transitions):
    nuevoConjunto = set(conjuntoActual) 

    for i in conjuntoActual:
        for j in transitions.keys():
            if j[0] == i and j[1] == '': 
                for k in transitions[(i, j[1])]:
                    nuevoConjunto.add(k)

    if nuevoConjunto != set(conjuntoActual):
        return formarSubconjunto(nuevoConjunto, transitions)
    else:
        return nuevoConjunto

def subconjuntos(afn):
    afnTransitions = afn.getTransitions()
    allchars = []

    afnTransitions2 = {}

    for i in afnTransitions:
        if i[1] == 'ε':
            afnTransitions2[(i[0],'')] = afnTransitions[i]
        else:
            afnTransitions2[i] = afnTransitions[i]

    afnTransitions = afnTransitions2

    for i in afnTransitions.keys():
        if i[1] != '':
            allchars.append(i[1])
    
    allchars = sorted(allchars)

    afnTransitions[(afn.getAccept(), '')] = [afn.getAccept()]

    states = []
    for i in afnTransitions.keys():
        states.append(i[0])

    allchars.append('')
    states.sort()

    sets = {}
    for i in states:
        for j in (allchars):
            if j == '':
                if ((i,j) in afnTransitions.keys()):
                    conjunto = copy.deepcopy(afnTransitions[(i,j)])
                    conjunto.append(i)
                    sets[i] = {'ε':formarSubconjunto(conjunto,afnTransitions)}
            else:
                if ((i,j) in afnTransitions.keys()):
                    sets[i] = {j:set(afnTransitions[(i,j)]),
                               'ε':set([i])}
                    
    for i in sets.values():
        if afn.getStart() in i['ε']:
            startNode = i['ε']

    startString = conjuntoToString(startNode)

    conjuntosAFD = []
    conjuntosAFD.append(startString)

    afdTransitions = {}

    changed = True
    while changed:
        changed = False
        for i in conjuntosAFD:
            for j in allchars:
                conjunto = set()
                for x in i.split(','):
                    x = int(x)
                    if j != '':
                        if (x,j) in afnTransitions:
                            for k in afnTransitions[(x,j)]:
                                for l in sets[k]['ε']:
                                    conjunto.add(l)

                if len(conjunto) > 0:
                    conString = conjuntoToString(conjunto)
                    afdTransitions[(i,j)] = conString
                    if conString not in conjuntosAFD:
                        conjuntosAFD.append(conString)
                        changed = True

    uppercase_alphabet = list(string.ascii_uppercase)

    translation = list(zip(list(conjuntosAFD),uppercase_alphabet))

    newTransitions = {}
    for i in afdTransitions:
        for j in translation:
            if i[0] == j[0]:
                newTransitions[(j[1],i[1])] = afdTransitions[i]

    newTransitions2 = {}
    for i in newTransitions:
        for j in translation:
            if newTransitions[i] == j[0]:
                newTransitions2[i] = j[1]


    nodosAcceptance = []

    for i in conjuntosAFD:
        if str(afn.getAccept()) in i:
            nodosAcceptance.append(i)

    for i in translation:
        if i[0] == startString:
            startString = i[1]

    nodosAcceptance2 = []
    for i in nodosAcceptance:
        for j in translation:
            if i == j[0]:
                nodosAcceptance2.append(j[1])

    allChars2 = []
    for i in allchars:
        if i not in allChars2 and i != '' and i != 'ε':
            allChars2.append(i)

    newTransitions = {}

    for i in newTransitions2:
        for j in allChars2:
            if (i[0],j) not in newTransitions2:
               # newTransitions[(i[0],j)] = 'V'
               # for k in allChars2:
               #     newTransitions[('V',k)] = 'V'
                a = 1
            else:
                newTransitions[(i[0],j)] = newTransitions2[(i[0],j)]
    return AFD(startString,nodosAcceptance2,newTransitions)

# Minimización
def minimizacion(afd):
    afdTransitions = afd.getTransitions() # Transiciones del AFD
    afdStart = afd.getStart() # Estado inicial del AFD
    afdAccept = afd.getAccept() # Estados de aceptación del AFD

    pi_0 = []
    non_accepting_states = [state for state, _ in afdTransitions.keys() if state not in afd.getAccept()]
    pi_0.append(non_accepting_states)   
    pi_0.append(afd.getAccept())

    allchars = sorted(list(set([char for _, char in afdTransitions.keys()])))

    while True:
        new_partitions = []
        
        for subset in pi_0:
            partitions = {} 

            for state in subset:
                key = tuple() 
                for char in allchars:
                    if (state, char) in afdTransitions:
                        destination = afdTransitions[(state, char)]
                        for index, category in enumerate(pi_0):
                            if destination in category:
                                key += (index,)
                                break
                    else:
                        key += (-1,) 

                if key not in partitions:
                    partitions[key] = []
                partitions[key].append(state)

            new_partitions.extend(partitions.values())

        if len(new_partitions) == len(pi_0): # Si no hubo cambios en las particiones entonces terminar
            break
        pi_0 = new_partitions

    new_partitions2 = []
    for i in pi_0:
        temp = []
        for j in i:
            if j not in temp:
                temp.append(j)

        if len(temp) > 0:
            new_partitions2.append(temp)

    pi_0 = new_partitions2

    simplified_transitions = {} # Construccion del AFD minimizado
    for char in allchars:
        for subset in pi_0:
            source_state = ','.join(subset)
            if (subset[0], char) in afdTransitions: 
                destination = afdTransitions[(subset[0], char)]
                for category in pi_0:
                    if destination in category:
                        simplified_transitions[(source_state, char)] = ','.join(category)
                        break

    simplifiedTransitions2 = {}
    for i in simplified_transitions:
        simplifiedTransitions2[(i[0][0],i[1])] = simplified_transitions[i][0]

    for i in simplifiedTransitions2:
        if i[0] == afdStart:
            afdStart = i[0]


    afdAcceptFinal = [] # Estados de aceptación del AFD minimizado

    for i in simplifiedTransitions2:
        if (i[0] in afdAccept) and (i[0] not in afdAcceptFinal):
            afdAcceptFinal.append(i[0])



    return AFD(afdStart,afdAccept,simplifiedTransitions2)

class AFD:
    def __init__(self, startNode, acceptanceNodes, transitions):
        self.startNode = startNode
        self.acceptanceNodes = acceptanceNodes
        self.transitions = transitions

    def getTransitions(self):
        return self.transitions
    def getStart(self):
        return self.startNode
    def getAccept(self):
        return self.acceptanceNodes

    def visualize(self):
        dot = Digraph('AFD')
        
        all_nodes = set()
        for (src, _), dest in self.transitions.items():
            all_nodes.add(src)
            all_nodes.add(dest)
        
        for node in all_nodes:
            if node in self.acceptanceNodes:
                dot.node(node, shape='doublecircle')
            else:
                dot.node(node)
        
        for (src, label), dest in self.transitions.items():
            dot.edge(src, dest, label=label)
        
        return dot
