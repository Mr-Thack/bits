# sections.py

class section:
    def __init__ (self,name,start,end,data,args):
        self.name=name
        self.start=start
        self.end=end
        self.data=data
        self.args=args
        # If args[0] is false
        # then we won't give it any args in modified assembly file

def retrieveSectAddr(disArray):
    # Set up start data because some data at start doesn't have a section
    name=""
    start=0
    end=0
    data=""
    args=[]
    ret=[]
    for i, line in enumerate(disArray):
        # First statement for end of disArray
        if (i == 0 or i+1==len(disArray) or
            line.startswith(".text") or line.startswith(".data")
            or line.startswith(".bss") or line.startswith(".section")):

            # START This section will end a section of assembly
            if not i==0:
                end=i
                if name == "end_section":
                    data.append(line)
                    # Add last line onto end if ending whole file
                nsection=section(name,start,end,data,args)
                ret.append(nsection)
                print("Found section end", name)

            # Clear vars
            # [BUG] won't work if .bss isn't last section
            if line == ".bss":
                name = "end_section"
                args = False
                start = i+1
                # Because i is "# end section .bss"
            else:
                name=""
                start=0
            end=0
            data=[]
            # END

            # Set name to section's name
            if (line.startswith(".section")):
                name=line[9:9+line.replace(".section ","").find(" ")]
                # [NOTE] ".section" is 9 characters; That long part on the end
                # splits of the .section and then find the address of the
                # " " (space) and adds 9 to get it's proper address
                # [NOTE] The extra 2 in the offset is to get rid of the comma
                # It's being split along commas and the 1st one shouldn't be there
                args=line[11+line.replace(".section ","").find(" "):].split(",")
            elif i == 0:
                name = "start_section"
                args=False
                # Add first line onto begining if starting file
                data.append(line)
            elif not name == "end_section" and not i+1==len(disArray):
                name=line
                args="NONE"

            start=i
            if not name == "":
                print("Found section start", name)
        else:
            # Add line onto data for section
            data.append(line)
    for i, sec in enumerate(ret):
        print("Section recorded", sec.name)
    return ret

def buildData(disArray):
    newData = ""
    for i, sect in enumerate(disArray):
            newData=newData+sect.args
            newData=newData+"\n"+sect.data
