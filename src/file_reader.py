def read_input(file_path):
    expressions = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if ',' in line:
                regex, string = line.split(',', 1)
                regex = regex.strip()
                string = string.strip()
                expressions.append((regex, string))
    return expressions
