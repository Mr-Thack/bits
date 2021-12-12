# sections.py

class section:
    def __init__ (self,name,start,end,data):
        self.name=name
        self.start=start
        self.end=end
        self.data=data

def retrieveSectAddr(disArray):
    name=""
    start=0
    end=0
    data=""
    ret=[]
    for i, line in enumerate(disArray):
        if (line.startswith(".text") or line.startswith(".data") or line.startswith(".bss") or line.startswith(".section")):
            if (line.startswith(".section")):
                name=line[9:9+line.replace(".section ","").find(" ")]
                # ".section" is 9 characters; That long part on the end
                # splits of the .section and then find the address of the first
                # " " (space) and adds 9 to get it's proper address
            else:
                name=line
                # so the name is whatever was put in before
                # ex: .text, .data, .bss
            print("Found section name : ", name)
            start=i
        elif (line.startswith("# end") and name==line[14:]):
            end=i
            nsection=section(name,start,end,data)
            data="" # Clear data
            print("Found end section: ", name)
            ret.append(nsection)
        elif (not name == ""):
            data=data+line+"\n"
    #for i in ret:
    #    print("Name:", i.name, ":Start:", i.start, ":End:", i.end, ":Data:", i.data)
    return ret


