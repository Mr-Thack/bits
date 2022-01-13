#!/usr/bin/python
import sys
import getopt

def args(argv):
    inputFile=""
    helpMsg="Usage: bits.py -f file.asm \nIt will then output file.arm.asm\n\nMade by bhaia, still not done\nWill convert AMD64 asm to ARM64 asm\n"
    try:
        opts, args = getopt.getopt(argv,"hf:",["file="])
    except getopt.GetoptError:
        print("bits.py -h")
        sys.exit(2)
    if len(sys.argv) == 1:
        print(helpMsg)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(helpMsg)
            sys.exit()
        elif opt in ("-f", "--file"):
            print("Input file is " + arg)
            inputFile = arg
        else:
            print("Wrong argument combination\n" + helpMsg)
            sys.exit(2)

    return inputFile
