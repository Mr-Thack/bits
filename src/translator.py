# Translates registers and compares against instructions on AMD64 binaries

import common
import registers
import instructions

def deparsePreProc(preProc):
    args = common.condense(preProc.args,", ")
    args = args[:len(args)-1]
    # It's in 2 instructions because we need len(args)
    # and if we try to do that before, we'll get it undefined
    return "." + preProc.ins + " " + args

def translateArgs(dataArray):
    newDataArray = []
    for l, line in enumerate(dataArray):
        if type(line) == common.instruction:
            argLine = []
            for a, arg in enumerate(line.args):
                if arg.argType == common.argTypes.register:
                    argLine.append(arg)
                elif arg.argType == common.argTypes.comp:
                    if type(arg.data) == common.compArgRegPoint:
                        argLine.append(common.compArgRegPoint(
                            arg.data.register,
                            arg.data.operation,
                            arg.data.pointer,
                            arg.data.isDereferenced))
                        print("translator.py : translateArgs() THIS", argLine[len(argLine)-1].register)
                else:
                    argLine.append(arg)
            newDataArray.append(common.instruction(line.ins,argLine))
        else:
            newDataArray.append(line)

    return newDataArray

def translateIns(dataArray):
    newDataArray = []
    for l, line in enumerate(dataArray):
        if type(line) == common.instruction:
            newArgs = []
            if line.ins == "pop":
                line.ins = "stp"
                newArgs.append(line.args[0])
                newReg = registers.registers[findReg("")]
    return dataArray

def translate(dataArray):
    newDataArray = []
    newDataArray = translateArgs(dataArray)
    newDataArray = translateIns(dataArray)

    return newDataArray
