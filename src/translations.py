# Lost all work on instructions.py and cleanup.py
# And all my good examples
# Time to redo
import common as com

class transrule:
    def __init__(self,amd,arm):
        self.amd = amd
        self.arm = arm
# AMD is the list of argTypes to be used
# ARM is the list of what to translate into

instructions = [
    transrule(
        com.instruction("push", [com.argTypes.register]),
        [com.instruction("stp", [
            "$1",
            com.register("ERROR_UNNAMED"),
            com.compArgRegInt(com.register("RSP"),"-",16,True,True)
        ])]
    ),
    transrule(
        com.instruction("mov", [com.argTypes.register, com.argTypes.register]),
        [com.instruction("mov", [
            "$1",
            "$2"
        ])]
    ),
    transrule(
        com.instruction("lea", [com.argTypes.register, com.argTypes.compArgRegInt]),
        [com.instruction("adrp",[
            "$1",
            "$2@1"]),
        com.instruction("add",[
            "$1",
            "$1",
            ":lo12:$2@1"]
        )]
    ),
    transrule(
        com.instruction("pop", [com.argTypes.register]),
        [com.instruction("ldp", [
            "$1",
            com.register("ERROR_UNNAMED"),
            com.compArgRegInt(com.register("RSP"),"+",16,False,True)
        ])]
    ),
    transrule(
        com.instruction("call",[com.argTypes.pointer]),
        [com.instruction("bl",[
            "$1"
        ])]
    ),
    transrule(
        com.instruction("ret",[]),
        [com.instruction("ret",[])]
    ),
    transrule(
        com.instruction("nop",[]),
        [com.instruction("nop",[])]
    )

]
