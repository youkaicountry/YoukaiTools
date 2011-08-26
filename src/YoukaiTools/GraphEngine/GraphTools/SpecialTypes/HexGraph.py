import math

sq3 = math.sqrt(3)
threeo2 = 3.0 / 2.0

def buildHexGraph(g, dimensions, sidelength=1.0):
    for b in range(-dimensions[2], dimensions[2]+1):
        for gr in range(-dimensions[1], dimensions[1]+1):
            for r in range(-dimensions[0], dimensions[0]+1):
                addVertexToHexGraph(g, (r, gr, b))
    return

def addVertexToHexGraph(g, vid, xpos="x", ypos="y"):
    if g.containsVertex(vid): return
    g.addVertex(vid)
    print(vid)
    g.setVertexData(vid, "x", sq3 * (vid[2]/2.0 + vid[0])) #x = sqrt(3) * s * ( b/2 + r)
    #g.setVertexData(vid, "x", -sq3 * (vid[2]/2.0 + vid[1])) #x = - sqrt(3) * s * ( b/2 + g )
    g.setVertexData(vid, "y", threeo2 * vid[2]) #y = 3/2 * s * b
    #find adjacent vertices
    adjacent = [(vid[0]-1, vid[1], vid[2]+1), (vid[0]+1, vid[1], vid[2]-1), (vid[0]-1, vid[1]+1, vid[2]), (vid[0]+1, vid[1]-1, vid[2]), (vid[0], vid[1]-1, vid[2]+1), (vid[0], vid[1]+1, vid[2]-1)]
    for v in adjacent:
        if g.containsVertex(v):
            g.addEdge(vid, v)
    return