# Backend : Backend for the ddisasm, and later we can add more
import os
import sys

def disassemble(fileName, fileOut):
    discmd = "ddisasm " + fileName + " --asm " + fileOut
    print("Running : " + discmd)
    output = os.system(discmd)
    if (output == "ERROR: dis.s: Binary format not supported."):
        print("NOT A BINARY")
        sys.exit()
    return True
