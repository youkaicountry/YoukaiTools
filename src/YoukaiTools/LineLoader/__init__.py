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

#load lines of values seperated by some character
def loadSep(f, comments=["#"], lstrip=True, rstrip=True, killblanks=True, valstrip=True, valsep=" ", killblankvals=True):
    lines = loadLines(f, comments, lstrip, rstrip, killblanks)
    out = []
    for l in lines:
        sep = l.split(valsep)
        if valstrip:
            sep = [s.strip() for s in sep]
        if killblankvals:
            sep = [s for s in sep if s != ""]
        out.append(sep)
    return out

def loadSepFilename(filename, comments=["#"], lstrip=True, rstrip=True, killblanks=True, valstrip=True, valsep=" ", killblankvals=True):
    f = open(filename, "r")
    l = loadSep(f, comments, lstrip, rstrip, killblanks, valstrip, valsep, killblankvals)
    f.close()
    return l

#make paramsep None to not have parameters
#put this in terms of loadSep
def loadConfig(f, comments=["#"], lstrip=True, rstrip=True, killblanks=True, assign="=", namestrip=True, valstrip=True, paramsep=" "):
    lines = loadLines(f, comments, lstrip, rstrip, killblanks)
    #further process into a dictionary
    data_dic = {}
    for l in lines:
        ls, rs = l.split(assign)
        if namestrip: ls = ls.strip()
        if valstrip: rs = rs.strip()
        params = [rs]
        if paramsep is not None:
            params = rs.split(paramsep)
            if killblanks:
                params = [p for p in params if p.strip() != ""]
        data_dic[ls] = params
    return data_dic

def loadConfigFilename(filename, comments=["#"], lstrip=True, rstrip=True, killblanks=True, assign="=", namestrip=True, valstrip=True, paramsep=" "):
    f = open(filename, "r")
    l = loadConfig(f, comments, lstrip, rstrip, killblanks, assign, namestrip, valstrip, paramsep)
    f.close()
    return l

