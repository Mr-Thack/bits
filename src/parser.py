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

class instruct:
    def __init__(self,ins,*args):
        self.ins = ins
        self.args = args
        self.length = len(args)

def parse(sectData):
    parsedData = []
    for i, line in enumerate(sectData):
        if line.endswith(":"):
            newLabel = label(line[:len(line)-2])
            parsedData.append(newLabel)
        elif line.startswith("."):
            line=line[1:].split(" ")
            newPreProc = preproc(line[0],line[1:])
        else:
            ins = line.split(" ")[0]
            argLine = line[line.find(" ")+1:]
            if ins == argLine:
                argLine = None
            else:
                argLine = argLine.split(",")
                args = []
                for a, arg in enumerate(argLine):
                    result = common.findReg(arg)
                    if result:
                        args.append(registers.AMD64Registers[result-1])
                argLine.append(args)
            #newLine=newLine[:len(newLine)-1]
            #ins = newLine[0]
            #args = newLine[1:]
            print(ins, argLine)
            #if ins == "nop":
            #    print(args[0].name)

    return parsedData
