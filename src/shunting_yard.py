def infix_to_postfix(expression):
    output = []
    operators = []
    precedence = {'*': 3, '.': 2, '|': 1, '(': 0}
    
    for char in expression:
        if char.isalnum() or char == 'ε':
            output.append(char)
        elif char == '(':
            operators.append(char)
        elif char == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()
        else:
            while operators and precedence[char] <= precedence[operators[-1]]:
                output.append(operators.pop())
            operators.append(char)
    
    while operators:
        output.append(operators.pop())
    return ''.join(output)
