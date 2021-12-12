# Parser : parses the disassembly output to remove unneeded information
#   Then sets it up as an array of a class
import sections
import instructions

def removeComments(data):
    outputArray = []
    # Put all lines that deserve to live in the new array
    for i, line in enumerate(data):
        # Keep only lines that have a comment and end section ...
        if (not line.startswith("#") or line.startswith("# end")):
            outputArray.append(line)
    return outputArray

def removeWhiteSpace(data):
    outputArray = []
    for i, line in enumerate(data):
        if (not line == ""):
            outputArray.append(line.strip())
    return outputArray

def removeCFI(data):
    outputArray = []
    for i, line in enumerate(data):
        outputArray.append(line)
    return outputArray

def condenseList(clist,char):
    # First arg is condense list because list is already defined
    data = ""
    # Just adds all the data into 1 string
    for i in clist:
        data=data+i+char
    return data

def condenseArray(array,char):
    data = ""
    for a in array:
        for b in a:
            data = data + b + " "
        data = data + char

    return data

def formatSections(sects):
    text=""
    for i in sects:
        text=text+"Name: "+i.name+"\nStart: "+str(i.start)+"\nEnd: "+str(i.end)+"\n{\n"+i.data+"}\n\n"
    return text

def parse(fileData):
    parsedData = fileData
    parsedData = parsedData.split('\n') # Split based on new line character

    parsedData = removeComments(parsedData)
    parsedData = removeWhiteSpace(parsedData)
    parsedData = removeCFI(parsedData)

    sectionData = sections.retrieveSectAddr(parsedData)
    # instructionData is the data from the .text section
    instructionData = instructions.parseInstructions(sectionData)
    # Format data before sending
    sectionData = formatSections(sectionData)
    parsedData = condenseList(parsedData,"\n")
    instructionData = condenseArray(instructionData, "\n")

    return parsedData, sectionData, instructionData
