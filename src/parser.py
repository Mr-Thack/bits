# Parser does parsing

import sys
import common
import registers# Call translate.translate()
import warnings

verboseCompArgs = ["QWORD", "PTR"]


def parse(sectData):
    parsedData = []
    for i, line in enumerate(sectData):
        if line.endswith(":"):
            # Must be a label
            newLabel = common.label(line[:len(line)-1])
            parsedData.append(newLabel)
        elif line.startswith("."):
            # If not label, must be an assembler preprocessor
            ins=line[1:].split(" ")[0] # Starting from 1 because 1 is "."
            argLine = line[len(ins)+1:].replace(" ", "").split(",")
            # Remove len of ins + 1 (it's a space), then delete all spaces and split by comma,
            newPreProc = common.preProc(ins,argLine)
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
                newArgNone = common.arguement(None, common.argTypes.none)
                # Make arg, make instruct, then append onto parsedData array
                newInstruction = common.instruction(ins,[newArgNone])
                parsedData.append(newInstruction)
            else:
                argLine = argLine.split(",")
                # Commas split each arg
                args = []
                for a, arg in enumerate(argLine):
                    if arg.isdigit():
                        # Arg must be a digit
                        newArgInt = common.arguement(int(arg),common.argTypes.integer)
                        args.append(newArgInt)
                    else:
                        result = common.findReg(arg)
                        if result != None: # See if arg is a register, and if so:
                            newArgReg = common.arguement(common.register(arg), common.argTypes.register)
                            args.append(newArgReg)
                        elif common.isAscii(arg): # Must be a label
                            # [NOTE] Checking for string is after checking for register
                            # Because, for example, "RBX" is a register, but it also happens to be a string
                            # Or QWORD PTR [RIP +._L2004] is a complex but it's also a string
                            if " " in arg or "+" in arg or "-" in arg or "*" in arg or "/" in arg:
                                # Must be a complex, because all of these complexes have space
                                # [TODO] Finish parse complex arg before appending it into array
                                compType = common.argTypes.comp # This is the type of comp arg
                                argData = arg.split(" ")
                                newArgData = ""

                                # Get rid of verbose pieces
                                for p, part in enumerate(argData):
                                    for w, word in enumerate(verboseCompArgs):
                                        # Removes verbose args that will be figured out by register size
                                        if word == part:
                                            # If found, set to Null
                                            part = None
                                    if not part == None:
                                        # If not found, then append
                                        newArgData = newArgData + part

                                # Above should return a string if all went fine
                                # [TODO] Add code for "-", "*" and "/"
                                isDereferenced = False
                                if newArgData.startswith("[") and newArgData.endswith("]"):
                                    # Find if dereferenced or not
                                    isDereferenced = True
                                    newArgData = newArgData[1:len(newArgData)-1]

                                # [TODO] Clean this stuff up
                                # It won't work for other types of comp args
                                if newArgData.find("+"):
                                    newArgData = newArgData.split("+")
                                    register = common.findReg(newArgData[0])
                                    if result == None:
                                        compType = common.argTypes.compArgRegPoint
                                        arg = common.compArgRegPoint(
                                            common.register(newArgData[0]), "+", common.pointer(newArgData[1]), isDereferenced)

                                newArgComplex = common.arguement(arg, compType)
                                args.append(newArgComplex)
                            else:
                                # Must be a pointer or a dereferenced pointer
                                # AKA a label
                                print(arg)
                                warnings.warn("This might be a new data type: ^ ")
                                newArgPoint = common.arguement(common.pointer(arg), common.argTypes.pointer)
                                args.append(newArgPoint)
                newInstruction = common.instruction(ins,args)
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

def deparseInstruction(instruct,curArchitecture):
    argLine = instruct.ins + " "

    for i, arg in enumerate(instruct.args):
        if arg.argType == common.argTypes.none:
            argLine = instruct.ins
        elif arg.argType == common.argTypes.integer:
            argLine = argLine + str(arg.data)
        elif arg.argType == common.argTypes.register:
            if curArchitecture == "AMD64":
                argLine = argLine + str(arg.data.reg.name)
            elif curArchitecture == "ARM64":
                argLine = argLine + str(arg.data.reg.equiv)
        elif arg.argType == common.argTypes.pointer:
            argLine = argLine + arg.data.relocation + str(arg.data.name)
        elif arg.argType == common.argTypes.compArgRegPoint or common.argTypes.compArgRegInt:
            # The above classes are quite similar
            # So we can do some similar things to them
            extraStartChar = ""
            extraEndChar = ""
            reg = ""
            sndPiece = ""
            # This is the 2nd piece,
            # So a pointer or an integer

            if arg.argType == common.argTypes.compArgRegPoint:
                sndPiece = str(arg.data.pointer.name)
            elif arg.argType == common.argTypes.compArgRegInt:
                sndPiece = str(arg.data.integer)

            if curArchitecture == "AMD64":
                reg = str(arg.data.reg.reg.name)
            elif curArchitecture == "ARM64":
                reg = str(arg.data.reg.reg.equiv)

            if arg.data.isDereferenced:
                extraStartChar = "["
                extraEndChar = "]"
                if arg.data.isPreincrement:
                    extraEndChar = "]!"

            if arg.data.isPreincrement:
                argLine = argLine + extraStartChar + reg + "," + arg.data.operation + sndPiece + extraEndChar
            else:
                argLine = argLine + extraStartChar + reg + extraEndChar + "," + arg.data.operation + sndPiece
            # [TODO] Finish making this actually do something
        else:
            print("Support for ", arg.argType)
            warnings.warn("^ not yet added in the parser!!!", UserWarning)
            sys.exit(1)
        if not i + 1 == len(instruct.args):
            argLine = argLine + ", "
    return argLine

def deparse(sectArray, arc):
    curArchitecture = arc
    newData = []
    for l, line in enumerate(sectArray):
        if type(line) == common.label:
            newData.append(deparseLabel(line))
        elif type(line) == common.preProc:
            newData.append(deparsePreProc(line))
        elif type(line) == common.instruction:
            newData.append(deparseInstruction(line,curArchitecture))
        else:
            print("Support for ", type(line), " not added for ", line, "!")

    return newData


