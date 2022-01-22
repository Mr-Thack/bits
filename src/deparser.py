# Screw deparses into what it looks like before lexing

import sys
import common
import registers# Call translate.translate()
import warnings

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
