#!/usr/bin/python
import args
import sys

import fileio
import parser
import backend

disassembledFile = "dis.s"

def main(argv):
    fileName = args.args(argv)
    backend.disassemble(fileName,disassembledFile)
    # Read the disassembled file
    fileData = fileio.readFile(disassembledFile)
    # Ask parser to do stuff
    parsedData, sectionData = parser.parse(fileData)
    # writeFile requires pre stringed data
    fileio.writeFile("mod.s", parsedData)
    fileio.writeFile("infofile", sectionData)
    #print("Data is : \n", parsedData)


if __name__ == "__main__":
    main(sys.argv[1:])
