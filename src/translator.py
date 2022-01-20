# Translates registers and compares against instructions on AMD64 binaries

import common
import registers
import instructions
import warnings

"""
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
"""

def translateIns(line):
    ret = []
    # [NOTE] The transrules found in instructions
    # Do not follow the rules in the rest of the program
    # The transrules DO NOT wrap the argument in common.arguement

    # Will be an array of instructions
    # These will be derived from the rules
    for r, rule in enumerate(instructions.instructions):
        # Try to match the instruction to conversion rules
        if line.ins == rule.amd.ins:
            orgargs = line.args
            for c, clause in enumerate(rule.arm):
                newArgs = []
                for a, arg in enumerate(clause.args):
                    # For all args, check if is string and has $
                    argType = None
                    newArg = None
                    if type(arg) == str:
                        if arg.find("$") != -1:
                            index = int(arg[arg.find("$")+1])
                            # If not found (because -1 is found)
                            if arg.find("@") != -1:
                                #property is 2nd part
                                prop = arg.split("@")[1]
                                argType = getattr(common.argTypes,prop)
                                newArg = common.arguement(getattr(orgargs[index-1].data,prop),argType)
                            else:
                                # Set arg to that index of orgargs
                                newArg = orgargs[index-1]
                                argType = newArg.argType
                    else:
                        newArg = arg
                        argType = common.typeToEnum(arg)
                    if type(newArg) == common.arguement:
                        # If the newArg is already an argument,
                        # Remove one argument layer wrapper,
                        # and we'll be good to go
                        warnings.warn("Might be an issue")
                        newArg = newArg.data
                    newArgs.append(common.arguement(newArg,argType))
                ret.append(common.instruction(clause.ins,newArgs))
    return ret

def translate(dataArray):
    newDataArray = []
    for l, line in enumerate(dataArray):
        # for line in dataArray, if it's an instruction
        if type(line) == common.instruction:
            newInstructions = translateIns(line)
            # This will return an array
            # So in the next loop we'll append things onto the newDataArray piece by piece
            for i, ins in enumerate(newInstructions):
                newDataArray.append(ins)

    return newDataArray

