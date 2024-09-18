# Universidad del valle de Guatemala
# Teoría de la computación
# Proyecto 1
# Carlos Valladares
# Gabriel Paz

from regex_functions import infixToPostfix, leerArchivo
from afn import armarAFN, AFN
from afd import subconjuntos, simplificarAFD, AFD
from simulacion import simularAFN, simularAFD
from graficar import graficarAFN, graficarAFD


def main():

    data = leerArchivo()

    for i in range(len(data)):
        print('##################################################################################################################')
        print(f'Trabajando con la regex {data[i]}\n')

        #Inciso 1 Construcción infix a postfix
        postfix = infixToPostfix(data[i])
        print(f'Conversión de infix a postfix: {postfix}')

        #Inciso2 formar el AFN de la regex
        print('Construcción del AFN...\n')
        afn = armarAFN(postfix)
        graficarAFN(afn,i)

        #Inciso 3 formar el AFD de la regex
        print('Construcción del AFD...\n')
        afd = subconjuntos(afn)
        graficarAFD(afd,i)

        #Inciso 4 formar el AFD simplificado de la regex
        print('Construcción del AFD simplificado...\n')
        afds = simplificarAFD(afd)
        graficarAFD(afds,i, True)

        print("Ingrese la cadena a probar:")  
        string = input()

        #Inciso 5 Simulaciín del AFN de la regex con la cadena
        print('Simulación del AFN')
        print(simularAFN(afn,string), '\n')

        #Inciso 6 Simulaciín del AFD de la regex con la cadena
        print('Simulación del AFD')
        print(simularAFD(afd,string), '\n')

        #Inciso 7 Simulaciín del AFD simplificado de la regex con la cadena
        print('Simulación del AFD simplificado')
        print(simularAFD(afds,string), '\n')

if __name__ == "__main__":
  main()