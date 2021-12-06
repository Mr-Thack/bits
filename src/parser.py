# Parser : parses the disassembly output to remove unneeded information
#   Then sets it up as an array of a class
import sections

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
        if (not line.startswith(".cfi")):
            outputArray.append(line)
    return outputArray

def modData(data):
    data = removeComments(data)
    data = removeWhiteSpace(data)
    data = removeCFI(data)
    return data

def condense(array,char):
    data = ""
    # Just adds all the data into 1 string
    for i in array:
        data=data+i+char
    return data

def formatSections(sects):
    text=""
    for i in sects:
        text=text+"Name: "+i.name+"\nStart: "+str(i.start)+"\nEnd: "+str(i.end)+"\n{\n"+i.data+"}\n\n"
    return text

def parse(fileData):
    parsedData = fileData
    parsedData = parsedData.split('\n') # Split based on new line character
    parsedData = modData(fileData)
    sectionData = sections.retrieveSectAddr(parsedData)

    # Format data before sending
    sectionData = formatSections(sectionData)
    parsedData = condense(parsedData,"\n")

    return parsedData, sectionData
