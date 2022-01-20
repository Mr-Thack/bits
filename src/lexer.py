# Lexer : lexes the disassembly output to put it into an array

def removeComments(data):
    outputArray = []
    # Put all lines that deserve to live in the new array
    for i, line in enumerate(data):
        # Keep only lines that have a comment and end section ...
        if (not line.startswith("#")):
            if line.find("@"):
                # I guess the @ is also a comment
                # Might as well remove it if found
                outputArray.append(line.split("@")[0])
            else:
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

# [BUG] This is a me issue
# Remove it soon
def removeInstructionsIDontWant(data):
    outputArray = []
    for i, line in enumerate(data):
        if line.find("nop") == -1:
            outputArray.append(line)
    return outputArray


def lex(fileData):
    lexedData = fileData
    lexedData = lexedData.split('\n') # Split based on new line character

    lexedData = removeComments(lexedData)
    lexedData = removeWhiteSpace(lexedData)
    lexedData = removeCFI(lexedData)
    lexedData = removeInstructionsIDontWant(lexedData)

    return lexedData
