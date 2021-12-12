import sys
import os

def readFile(fileName):
    doesExist = os.path.exists(fileName)
    if (doesExist == False):
        sys.exit()
    fileObj = open(fileName,"r")
    fileData = fileObj.read()
    fileObj.close()

    return fileData

def writeFile(fileName, data):
    doesExist = os.path.exists(fileName)
    if (doesExist == True):
        os.remove(fileName)
    f = open(fileName, "a")
    f.write(data)
    f.close()
