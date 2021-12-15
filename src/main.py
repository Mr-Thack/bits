#!/usr/bin/python
import args
import sys

import fileio
import lexer
import backend
import sections
import common
import parser

disassembledFile = "dis.s"
modFile = "mod.s"
sectionFile = "sections.data"
outDir = "out/" # You can change to ./ to make it output into current dir

def main(argv):
    fileName = args.args(argv)
    backend.disassemble(fileName,disassembledFile)
    # Read the disassembled file
    fileData = fileio.readFile(disassembledFile)
    # Ask lexer to do extract assembly
    lexedData = lexer.lex(fileData)
    # Then use sections to go through and retrieve sect addresses
    sectionData = sections.retrieveSectAddr(lexedData)
    # Then classify all preprocessor instructions
    # and labels, and processor instructions
    parsedData = parser.parse(sectionData[common.sectFind(sectionData,".text")].data)

    # writeFile requires pre stringed data
    fileio.mkdir(outDir)
    fileio.writeFile(outDir + modFile, common.sectCondense(sectionData))
    fileio.writeFile(outDir + sectionFile, common.sectFormat(sectionData))


if __name__ == "__main__":
    main(sys.argv[1:])
