from utilidades import Stack

def leerArchivo():
    archivo = open("input/expressions.txt", "r", encoding='utf-8')
    datos = archivo.read()
    archivo.close()
    return datos.split("\n")

def getPrecedence(char):
    if char == '(':
        return 1
    elif char == '|':
        return 2
    elif char == '.':
        return 3
    elif char in ['?','*','+']:
        return 4
    elif char == '^':
        return 5
    else:
        return 6
 
def infixToPostfix(regex: str):
    formatedRegex: str = formatRegex(regex)
    
    postfix: str = ''
    stack = Stack()
    escapeNextChar = False

    #Algoritmo de shunting yard con \ considerado
    for i in range(len(formatedRegex)):
        char1 = formatedRegex[i]
        
        if escapeNextChar:
            postfix += char1
            escapeNextChar = False
            continue

        if char1 == '\\':
            escapeNextChar = True
            continue

        if char1 == '(':
            stack.push(char1)
        elif char1 == ')':
            while stack.peek() != '(':
                postfix += stack.pop()
            stack.pop()
        else:
            while (not stack.isEmpty()):
                peekedchar = stack.peek()
                peekedCharPrecedence = getPrecedence(peekedchar)
                char1Precedence = getPrecedence(char1)
                if peekedCharPrecedence >= char1Precedence:
                    postfix += stack.pop()
                else:
                    break
            stack.push(char1)

    while (not stack.isEmpty()):
        postfix += stack.pop()                

    return postfix

def tranformOpt(string):
    stack = []
    for char in string:
        if char != '?':
            stack.append(char)
        else:
            temp = ''
            if len(stack) > 0 and stack[-1] == ')':
                count = 1
                temp = stack.pop() + temp
                while count > 0:
                    if stack[-1] == ')':
                        count += 1
                    elif stack[-1] == '(':
                        count -= 1
                    temp = stack.pop() + temp
                temp = temp[1:-1]
            elif len(stack) > 0 and (stack[-1] not in '()*|'):
                while len(stack) > 0 and (stack[-1] not in '()*|'):
                    temp = stack.pop() + temp
            else:
                continue
            temp = r'(ε|' + temp + ')'
            stack.append(temp)
    return ''.join(stack)

def tranformClass(regex):
    regexX = ''
    flag = False
    for i in range(len(regex)):
        char1 = regex[i]
        if i+1 < len(regex):
            char2 = regex[i+1]
            if flag:
                if char2 == ']':
                    regexX += char1
                    regexX += ')'
                    flag = False
                else:
                    regexX += char1
                    regexX += '|'
            if not flag:
                if char1 == '[':
                    regexX += '('
                    flag = True
                elif char1 == ']' or char2 == ']':
                    pass
                else:
                    regexX += char1    
    regexX += regex[-1]   

    return regexX

def transformPosKleene(regex):
    output = ''
    balanceStack = Stack()
    stack = Stack()
    posKleene = False
    for i in range(len(regex)):
        char1 = regex[(len(regex)-1)-i]

        if char1 == '+':
            posKleene = True
            continue

        if posKleene == True:
            stack.push(char1)

            if char1 == ')':
                balanceStack.push(char1)
            elif char1 == '(':
                balanceStack.pop()

            if balanceStack.isEmpty():
                substring = '('
                while not stack.isEmpty():
                    substring += stack.pop()
                substring += substring + ')*' + ')'
                output = substring + output
                posKleene = False
        else:
            output = char1 + output

    return output

def escapeChars(regex):
    output = ''
    for i in range(len(regex)):
        char1 = regex[i]
        if i+1 < len(regex):
            if char1 == '\\' and regex[i+1] not in ['(',')','{','}']:
                output += '\\'
                output += char1
            else:
                output += char1
    output += regex[-1]

    return output


def considerPeriod(regex):
    result = ''
    for i in range(len(regex)):
        chara1 = regex[i]
        if i+1 < len(regex):
            if chara1 == '.':
                result += '\\'
                result += chara1
            else:
                result += chara1
    result += regex[-1]
    return result

def formatRegex(regex: str) -> str:
    allOperators = ['|', '?', '+', '*', '^']
    binaryOperators = ['|', '^']
    res = ''

    #Cada clase se convierte en secuencia de or's
    regexX = tranformClass(regex)

    #Transformar el caracter ?
    regexX = tranformOpt(regexX)

    #Tomar en cuenta el operador '+'
    regexX = transformPosKleene(regexX)

    #Escapar el caracter backslash y escapar su si
    regexX = escapeChars(regexX)

    #Tomar en cuenta el caracter 'punto'
    regexX = considerPeriod(regexX)

    #Formato: Agregar punto de concatenación
    escaped = False

    for i in range(len(regexX)):
        c1 = regexX[i]
        if i+1 < len(regexX):
            c2 = regexX[i+1]
            res += c1
            if c1 == '\\' and not escaped:
                escaped = True
                continue

            if (escaped) and (c2 != ')') and (c2 not in allOperators):
                res += '.'
                escaped = False
                continue

            if (c1 != '(') and (c2 != ')') and (c2 not in allOperators) and (c1 not in binaryOperators) and (c1 != '\\') and (not escaped):
                res += '.'    
            
    res += regexX[-1]
    return res
