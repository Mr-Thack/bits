import sys
import os
import shutil


# Change outDir to "./" to make it come out in cur work dir
# The / is required at the end
outDir = "out/"
files = {
    "disFile" : "dis.s",
    "modFile" : "mod.s",
    "sectFile" : "sections.data"
}

for i, prop in enumerate(files):
    files[prop] = outDir+files[prop]

def mkdir(dirName):
    doesExist = os.path.exists(dirName)
    if (doesExist == True):
        shutil.rmtree(dirName)
    os.mkdir(dirName)

def readFile(fileName):
    doesExist = os.path.exists(fileName)
    if (doesExist == False):
        print("ERROR: " + fileName + " was deleted. It shouldn't have been deleted!")
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
