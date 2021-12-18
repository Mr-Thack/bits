# Registers.py
# All stuff dealing with registers
class reg:
    def __init__(self, name, equiv, size):
        self.name = name
        self.equiv = equiv
        self.size = size

registers = [
    reg("RBP","fp",64),
    reg("RSP","sp",64),
    reg("RAX","x0",64), # In SYS V AMD64 EABI, RAX is first return
    reg("RDI","x0",64), # and RDI is first paramter, this will be confusing to redo in ARM
    reg("EAX","w0",32),
    reg("RIP","pc",64)
]
