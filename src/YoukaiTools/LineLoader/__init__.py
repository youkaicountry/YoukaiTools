#append things to end
#block comments

def loadLines(f, comments=["#"], lstrip=True, rstrip=True, killblanks=True):
    l = f.readlines()
    if comments==None: com=[]
    else: com=comments
    for c in com:
        l = [x.split(c)[0] for x in l]
    if lstrip and rstrip:
        l = [x.strip() for x in l]
    else:
        if lstrip:
            l = [x.lstrip() for x in l]
        elif rstrip:
            l = [x.rstrip() for x in l]
    if killblanks:
        l = [x for x in l if x != ""]
    return l

def loadLinesFilename(filename, comments=["#"], lstrip=True, rstrip=True, killblanks=True):
    f = open(filename, "r")
    l = loadLines(f, comments, lstrip, rstrip, killblanks)
    f.close()
    return l

