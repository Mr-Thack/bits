# Translates registers and compares against instructions on AMD64 binaries

import common
import registers
import instructions
import warnings
import copy

def getPropsFromComp(arg):
    # Takes the argument to an instruction
    args = []
    types = []
    ret = [args,types]

    # Basically, this is an alias
    data = arg.data

    args.append(data.reg)
    types.append(common.argTypes.register)
    if type(data) == common.compArgRegPoint:
        args.append(data.pointer)
        types.append(common.argTypes.pointer)
    elif type(data) == common.compArgRegInt:
        args.append(data.integer)
        types.append(common.argTypes.integer)
    # Returns 2 subarrays
    # [args,types]
    return ret

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
                                sndIndex = int(arg[arg.find("@")+1])
                                # sndIndex is the 2nd part of the property
                                # after the @
                                props = getPropsFromComp(orgargs[index-1])

                                # IF there is an error somewhere around here
                                # That's because my type checking system is not yet implemented
                                newArg = copy.deepcopy(props[0][sndIndex])
                                argType = props[1][sndIndex]
                            else:
                                # Set arg to that index of orgargs
                                newArg = copy.deepcopy(orgargs[index-1])
                                argType = newArg.argType
                            if arg.find(":") != -1:
                                # The reason why we add 2 instead of 1,
                                # is because 1 is the normal offset, and
                                # 1 more because we are "shifting" the string by 1
                                newArg.relocation = arg[arg.find(":"):arg[1:].find(":")+2]
                    else:
                        newArg = arg
                        argType = common.typeToEnum(arg)
                    if type(newArg) == common.arguement:
                        # If the newArg is already an argument,
                        # Remove one argument layer wrapper,
                        # and we'll be good to go
                        warnings.warn("Might be an issue, seems arg inside of arg where shouldn't be")
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
        elif type(line) == common.preProc:
            if line.ins != "byte":
                newDataArray.append(line)
        elif type(line) == common.label:
            newDataArray.append(line)
        else:
            print(type(line), "Not working")

    return newDataArray

