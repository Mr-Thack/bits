# Parser does parsing

import sys
import common
import registers

class preProc:
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
            newLabel = label(line[:len(line)-1])
            parsedData.append(newLabel)
        elif line.startswith("."):
            # If not label, must be an assembler preprocessor
            ins=line[1:].split(" ")[0] # Starting from 1 because 1 is "."
            argLine = line[len(ins)+1:].replace(" ", "").split(",")
            # Remove len of ins + 1 (it's a space), then delete all spaces and split by comma,
            newPreProc = preProc(ins,argLine)
            parsedData.append(newPreProc)
        else:
            # Must be some type of data
            ins = line.split(" ")[0] # Make into array
            argLine = line[line.find(" ")+1:]
            # Take everything but first element (because instruction is first element)
            if ins == argLine:
                # [NOTE] Due to how python deals with strings,
                # if nothing is found and I add one, I get the first term back
                # try making a better method of finding if there's no arg later
                newArgNone = arguement(None, common.argTypes.none)
                # Make arg, make instruct, then append onto parsedData array
                newInstruction = instruction(ins,[newArgNone])
                parsedData.append(newInstruction)
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
                            # Or QWORD PTR [RIP +._L2004] is a complex but it's also a string
                            if " " in arg or "+" in arg or "-" in arg or "*" in arg or "/" in arg:
                                # Must be a complex, because all of these complexes have space
                                # [TODO] Parse complex arg before appending it into array
                                newArgComplex = arguement(arg, common.argTypes.comp)
                                args.append(newArgComplex)
                            else: # Must be a pointer or a dereferenced pointer
                                newArgPoint = arguement(arg, common.argTypes.pointer)
                                args.append(newArgPoint)
                                print("WARNING: this might be a new data type: [parser.py]", arg)

                newInstruction = instruction(ins,args)
                parsedData.append(newInstruction)

    return parsedData


# Return label name + :
def deparseLabel(label):
    return label.name + ":"

# Return deparsed preProc
def deparsePreProc(preProc):
    args = common.condense(preProc.args,", ")
    args = args[:len(args)-1]
    # It's in 2 instructions because we need len(args)
    # and if we try to do that before, we'll get it undefined
    return "." + preProc.ins + " " + args

def deparseInstruction(instruct):
    argLine = instruct.ins + " "

    for i, arg in enumerate(instruct.args):
        if arg.argType == common.argTypes.none:
            argLine = instruct.ins
        elif arg.argType == common.argTypes.integer:
            argLine = argLine + str(arg.data)
        elif arg.argType == common.argTypes.register:
            argLine = argLine + str(arg.data.name)
        elif arg.argType == common.argTypes.pointer:
            argLine = argLine + str(arg.data)
        elif arg.argType == common.argTypes.comp:
            argLine = argLine + str(arg.data)
            # [TODO] Make this actually do something
        else:
            print("Support for ", arg.argType, " not added in arguement types!")
            sys.exit(1)
        if not i + 1 == len(instruct.args):
            argLine = argLine + ", "
    return argLine

def deparse(sectArray):
    newData = []
    for l, line in enumerate(sectArray):
        if type(line) == label:
            newData.append(deparseLabel(line))
        elif type(line) == preProc:
            newData.append(deparsePreProc(line))
        elif type(line) == instruction:
            newData.append(deparseInstruction(line))
        else:
            print("Support for ", type(line), " not added for ", line, "!")

    return newData


