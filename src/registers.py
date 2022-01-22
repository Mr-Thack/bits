# Registers.py
# All stuff dealing with registers
class reg:
    def __init__(self, name, equiv, size):
        self.name = name
        self.equiv = equiv
        self.size = size

registers = [
    reg("RBP","fp",64),
    reg("ERROR_UNNAMED","x30",64), # ERROR_UNNAMED
    # BECAUSE THIS IS TESTING
    # RENAME TO PROPER x86 REGISTER WHEN DONE TESTING
    reg("RSP","sp",64),
    reg("RAX","x18",64),
    reg("EAX","w0",32),
    reg("RDI","x0",64),
    # In SYS V Architecture, RAX is first return
    # and RDI is first paramter,
    # so, I decided to just dump return in x18
    reg("RIP","pc",64),

]
