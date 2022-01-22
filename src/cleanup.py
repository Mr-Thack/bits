
def cleanlex(lexedData):
    # Don't even know what I'm doing here
    # Oh wait we're remove .intel_syntax noprefix
    stuffToRemove = [
        ".intel_syntax"
    ]
    newData = []
    for l, line in enumerate(lexedData):
        for s, stuff in enumerate(stuffToRemove):
            if line.find(stuff) == -1:
                newData.append(line)
    return newData

def removeSectionsIDontWant(sectionData):
    wantedSects = [".text",".rodata"]
    newData = []
    for s, section in enumerate(sectionData):
        for w, wanted in enumerate(wantedSects):
            if section.name == wanted:
                newData.append(section)
    return newData
