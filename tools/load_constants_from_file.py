def load_constants_from_file(file_name):
    
    constants = {}
    
    f  = open(file_name, 'r')

    for line in f:
        if line != "\n":
            key = line.split()[0]
            value = float(line.split()[-1])
            constants[key] = value

    f.close()
    
    return constants