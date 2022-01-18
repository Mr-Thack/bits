#!/usr/bin/python
import args
import sys

import fileio as files
import lexer
import backend
import sections
import common
import parser


## CONFIG ##
# File names stored in fileio.py

def main(argv):
    fileName = args.args(argv)

    # Make the outDir for all created files to be in
    files.mkdir(files.outDir)

    # Send the name of the disFile to the disassembler
    backend.disassemble(fileName,files.files["disFile"])

    # Read the disassembled file
    fileData = files.readFile(files.files["disFile"])

    # Ask lexer to do extract assembly
    lexedData = lexer.lex(fileData)

    # Then use sections to go through and retrieve sect addresses
    sectionData = sections.retrieveSectAddr(lexedData)

    # Then classify all preprocessor instructions
    # and labels, and processor instructions
    # only of the .text section
    parsedData = parser.parse(sectionData[common.sectFind(sectionData,".text")].data)

    # Call translate.translateRegisters
    #parsedData = translator.translate(parsedData)

    # deparse data to output into modified assembly file
    deParsedData = parser.deparse(parsedData, "AMD64")
    # Change AMD64 to ARM64 to get the ARM version
    sectionData[common.sectFind(sectionData,".text")].data = deParsedData
    # set section .text data as deParsedData


    # writeFile requires pre stringed data
    files.writeFile(files.files["modFile"], common.sectCondense(sectionData))
    files.writeFile(files.files["sectFile"], common.sectFormat(sectionData))


if __name__ == "__main__":
    main(sys.argv[1:])
