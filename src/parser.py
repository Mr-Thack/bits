# Parser does parsing

import common
import registers

class preproc:
    def __init__(self,ins,args):
        self.ins = ins
        self.args = args
        self.length = len(args)

class label:
    def __init__(self,name):
        self.name = name

class arguement:
    def __init__(self, data, argType):
        self.data = data
        self.argType = argType

class instruction:
    def __init__(self,ins,args):
        self.ins = ins
        self.args = args
        self.length = len(args)

def parse(sectData):
    parsedData = []
    for i, line in enumerate(sectData):
        if line.endswith(":"):
            # Must be a label
            newLabel = label(line[:len(line)-2])
            parsedData.append(newLabel)
        elif line.startswith("."):
            # If not label, must be an assembler preprocessor
            line=line[1:].split(" ")
            newPreProc = preproc(line[0],line[1:])
            parsedData.append(newPreProc)
        else:
            # Must be some type of data
            ins = line.split(" ")[0] # Make into array
            argLine = line[line.find(" ")+1:]
            # Take everything but first element (because instruction is first element)
            if ins == argLine:
                # [NOTE] Due to how python deals with strings,
                # if nothing is found and I add one, I get the first term back
                # try making a better method of doing this later
                argLine = None
            else:
                argLine = argLine.split(",")
                # Commas split each arg
                args = []
                for a, arg in enumerate(argLine):
                    if arg.isdigit():
                        # Arg must be a digit
                        newArgInt = arguement(int(arg),common.argTypes.integer)
                        args.append(newArgInt)
                    else:
                        result = common.findReg(arg)
                        if result: # See if arg is a register, and if so:
                            newArgReg = arguement(registers.AMD64Registers[result-1], common.argTypes.register)
                            args.append(newArgReg)
                        elif common.isAscii(arg): # Must be a label
                            # [NOTE] Checking for string is after checking for register
                            # Because, for example, "RBX" is a register, but it also happens to be a string
                            # Or QWORD PTR [RIP +._L2004] is a complex but it's also
                            if " " in arg: # Must be a complex
                                # [TODO] Parse complex arg before appending it into array
                                newArgComplex = arguement(arg, common.argTypes.comp)
                                args.append(newArgComplex)
                            else: # Must be a pointer or a dereferenced pointer
                                newArgPoint = arguement(arg, common.argTypes.pointer)
                                args.append(newArgPoint)

                newInstruction = instruction(ins,args)
                parsedData.append(newInstruction)

    return parsedData
