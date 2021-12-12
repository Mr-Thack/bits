# Translates sections.data and compares against instructions on AMD64 binary

def translate(data):
    data = translateRegisters(data)
