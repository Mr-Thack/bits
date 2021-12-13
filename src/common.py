# Common.py

def condense(array,char,alignStart=True):
    # alignStart is for adding char at begining or at end
    data = ""
    # Just adds all the data into 1 string
    for i in array:
        if alignStart:
            data=data+i+char
            # Removes extra char at end
        else:
            data=data+char+i
    if alignStart:
        data=data[0:len(data)-1]
    # [NOTE] there will be extra char at end of daya
    # The fix is remove one (extra) char
    return data


def sectFormat(sects):
    text=""
    for i in sects:
        args=""
        if not i.args == False and not i.args == "NONE":
            args=condense(i.args,",",)
        else:
            args="NONE"
        text=text+"Name: "+i.name+"\nArgs:"+args+"\nStart: "+str(i.start)+"\nEnd: "+str(i.end)+"\n{\n"+i.data+"}\n\n"
    return text

def sectCondense(sects):
    text=""
    for i in sects:
        if not i.args == False:
            args=".section " + i.name + " "
            if not i.args == "NONE":
                args=args+condense(i.args,",",False)
            args=args+"\n"
        else:
            args = ""
        text=text+args+i.data
    return text
