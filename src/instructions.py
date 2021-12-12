# Instructions.py


# [NOTE] This section is for different types of data types in assembly
# ASsembly INStructions
class asins:
    def __init__(self, ins, *ops):
        self.ins = ins

# CPU INStructions
class cpuins:
    def __init__(self, ins, *ops):
        self.ins = ins
        self.len = len(ops)
        newops = [""]
        for i, op in ops:
            if (op == ","):
                newops.append("")
            else:
                print(newops[len(newops)-1])

# Labels
class label:
    def __init__(self,name):
        self.name = name

def parseToArray(data,textSection):
    # Split based on new line into array
    data = textSection.data.split("\n")
    newData = []

    for i, line in enumerate(data):
        # We replace "," with " , " because we want to split the comma too
        line = line.replace(",", " , ").split(" ");
        newLine = []
        for a, text in enumerate(line):
            # Search for things like "", which we shouldn't have and get rid of it
            # AKA ensure only real data comes in
            if (not text == ""):
                newLine.append(text)
        if (not newLine == [] and not newLine == ['']):
            # Check if line is empty
            newData.append(newLine)

    return newData

def getins(data):
    newData = []
    classData = []
    for i, line in enumerate(data):
        # if not first character of line is .
        if line[0].endswith(":"):
            newlabel = label(line[0][:len(line[0])-2]
        elif line[0][0] == ".":
            arguements = [""]
            for a, arg in enumerate(line[1:]):
                if (arg == ","):
                    # Commas signal next arg
                    arguements.append("")
                else:
                    # Assume arguements[len(arguements)-1] is carg
                    if (arguements[len(arguements)-1] == ""):
                        # If carg is empty set as arg
                        arguements[len(arguements)-1] = arg
                    else:
                        # Else append arg with carg
                        arguements[len(arguements)-1] = arguements[len(arguements)-1] + " " +  arg
            print(line[0], arguements)
        #else:
        # [TODO] this doesn't do anything yet
        #    newinstruct = asins(line[0],line[1])
    return newData


def parseInstructions(dataArray):
    data = []
    textSection = ""
    # Find text section
    for i, sect in enumerate(dataArray):
        if (sect.name == ".text"):
            textSection = sect

    data = parseToArray(data,textSection)
    text = getins(data)

    return data#text
