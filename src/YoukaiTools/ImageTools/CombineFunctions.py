def paint(p1, p2):
    return p2[:]

def multiply(p1, p2):
    out = []
    for i,c in enumerate(p1):
        #print(i, c, p2[i])
        out.append(c*p2[i])
    return out

def average(p1, p2, weight1, weight2):
    div = weight1+weight2
    out = []
    for i, c in enumerate(p1):
        out.append(((c*weight1) + (p2[i]*weight2))/div)
    return out

def add(p1, p2, top=1.0):
    out = []
    for i,c in enumerate(p1):
        #print(i, c, p2[i])
        a = c+p2[i]
        if a > top: a = top
        out.append(a)
    return out
