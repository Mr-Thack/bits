# Registers.py
# All stuff dealing with registers
class reg:
    def __init__(self, name, size):
        self.name = name
        self.size = size

AMD64Registers = [
    reg("RBP",64),
    reg("RSP",64),
    reg("RAX",64),
    reg("RDI",64),
    reg("EAX",32)

]
