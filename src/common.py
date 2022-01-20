# Common.py
import registers
import enum
import warnings

class preProc:
    def __init__(self,ins,args):
        self.ins = ins
        self.args = args
        self.length = len(args)

class label:
    def __init__(self,name):
        self.name = name

class pointer:
    def __init__(self,name,isDereferenced=True):
        self.name = name
        self.isDereferenced = isDereferenced

class arguement:
    def __init__(self, data, argType):
        self.data = data
        self.argType = argType

class register:
    def __init__(self,reg,isPointing=False):
        print("Using",reg)
        self.reg = reg
        self.isPointing = isPointing

class compArgRegPoint:
    # Operation can be a string of "+", "-", "*", or "/"
    # computeArgument Register Pointer (AKA label such as ".L_2004")
    def __init__(self,register,operation,pointer,isDereferenced=False):
        self.register = register
        self.operation = operation
        self.pointer = pointer
        self.isDereferenced = isDereferenced

class compArgRegInt:
    def __init__(self,register,operation,integer,isDereferenced=False):
        self.register = register
        self.operation = operation
        self.integer = integer
        self.isDereferenced = isDereferenced

class instruction:
    def __init__(self,ins,args):
        self.ins = ins
        self.args = args
        self.length = len(args)

def condense(array,char,alignStart=True):
    # alignStart is for adding char at begining or at end
    data = ""
    # Just adds all the data into 1 string
    for i in array:
        if alignStart:
            data=data+i+char
            # Removes extra char at end
        else:
            data=data+char+i
    if alignStart:
        data=data[0:len(data)-1]
    # [NOTE] there will be extra char at end of daya
    # The fix is remove one (extra) char
    return data


# Formats sects for data file
def sectFormat(sects):
    text=""
    for i in sects:
        args=""
        if not i.args == False and not i.args == "NONE":
            args=condense(i.args,",",)
        else:
            args="NONE"
        text=text+"Name: "+i.name+"\nArgs:"+args+"\nStart: "+str(i.start)+"\nEnd: "+str(i.end)+"\n{\n"+condense(i.data,"\n")+"\n}\n\n"
    return text

# Finds number of wanted section
def sectFind(sects, sectName):
    for i, sect in enumerate(sects):
        if sect.name == sectName:
            return i

# Condenses sect for assembly file
def sectCondense(sects):
    text=""
    for i in sects:
        if not i.args == False:
            args=".section " + i.name + " "
            if not i.args == "NONE":
                args=args+condense(i.args,",",False)
            args=args+"\n"
        else:
            args = ""
        text=text+args+condense(i.data,"\n")+"\n"
    return text

# Returns the position of a register in the AMD64Registers array + 1
# This is because python will treat 0 the same None
# Basially None = Null
def findReg(name):
    for i, reg in enumerate(registers.registers):
        if reg.name == name:
            return i + 1
    print("WARNING [MAYBE UNIMPLEMENTED]: Register not found", name, "[common.py 91]")
    return None

def getReg(name):
    res = findReg(name)
    if res:
        return registers.registers[res-1]
    else:
        return None

# instructArguements
# Enum class for types of arguements for instructions
class argTypes(enum.Enum):
    none = 1
    integer = 2
    register = 3
    pointer = 4
    compArgRegInt = 5
    compArgRegPoint = 6
    comp = 7 # Reserved in case of issue

def typeToEnum(obj):
    # [NOTE]
    # Only implement what I actually need
    # So, no pointer or register or integer, if I don't need them
    if type(obj) == compArgRegInt:
        return argTypes.compArgRegInt
    elif type(obj) == compArgRegPoint:
        return argTypes.compArgRegPoint
    elif type(obj) == registers.reg:
        return argTypes.register
    elif type(obj) == int:
        return argTypes.integer
    else:
        print("Issue with", obj)
        warnings.warn("Most likely an uninmplemented error",FutureWarning)
        return None

def isAscii(s): # s stands for string
    # c stands for character
    return all(ord(c) < 128 for c in s)
    # making variables names shorter makes program faster (;
