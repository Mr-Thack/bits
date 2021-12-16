#!/usr/bin/python
import args
import sys

import files as files
import lexer
import backend
import sections
import common
import parser

outDir = "out/"
"""
You can change to ./ to make it output all files into current dir
But, you'll need a / at the end for it to work
"""


def main(argv):
    fileName = args.args(argv)

    files.setFileLocation(outDir)

    # Make the outDir for all created files to be in
    files.mkdir(fileio.outDir)

    # Send the name of the disFile to the disassembler
    backend.disassemble(fileName,files.files["disFile"])

    # Read the disassembled file
    fileData = files.readFile(fileio.files["disFile"])

    # Ask lexer to do extract assembly
    lexedData = lexer.lex(fileData)

    # Then use sections to go through and retrieve sect addresses
    sectionData = sections.retrieveSectAddr(lexedData)

    # Then classify all preprocessor instructions
    # and labels, and processor instructions
    parsedData = parser.parse(sectionData[common.sectFind(sectionData,".text")].data)

    # writeFile requires pre stringed data
    #print(files.files["modFile"])
    files.writeFile(fileio.files["modFile"], common.sectCondense(sectionData))
    files.writeFile(fileio.files["sectFile"], common.sectFormat(sectionData))


if __name__ == "__main__":
    main(sys.argv[1:])
