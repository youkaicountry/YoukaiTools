#Copyright (c) <2011> <Nathaniel Caldwell>

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from YoukaiTools import MazeGen

#id_list should be like [(1,2), (1,3), (2,2), ...]
def buildGridGraph(g, id_list=None, dimensions=None):
    if (id_list is None) and (dimensions is None):
        return
    elif (id_list is None) and (dimensions is not None):
        id_list = []
        for y in range(dimensions[1]):
            for x in range(dimensions[0]):
                id_list.append((x, y))
    elif (id_list is not None) and (dimensions is not None):
        return
    for vid in id_list:
        addVertexToGridGraph(g, vid)
    return

def buildGridGraphFromBlockMap(g, blockmap, unblocked=None):
    d = blockmap.getSize()
    for y in range(d[1]):
        for x in range(d[0]):
            if blockmap.getSpace(x, y) == unblocked:
                addVertexToGridGraph(g, (x, y))
    return
    
def addVertexToGridGraph(g, vid):
    if g.containsVertex(vid): return
    g.addVertex(vid)
    g.setVertexData(vid, "x", vid[0])
    g.setVertexData(vid, "y", vid[1])
    #find adjacent vertices
    adjacent = [(vid[0], vid[1]+1), (vid[0], vid[1]-1), (vid[0]-1, vid[1]), (vid[0]+1, vid[1])]
    for v in adjacent:
        if g.containsVertex(v):
            g.addEdge(vid, v)
    return

def gridInGrid(g, cg, size):
    gvl = []
    for v in cg.getVertexList():
        xmin = v[0] * size[0] * 2
        ymin = v[1] * size[1] * 2
        for y in range(size[1]):
            for x in range(size[0]):
                gvl.append((x + xmin, y + ymin))
    
    for e in cg.getEdgeList():
        ei = cg.getEdgeInfo(e)
        p1 = ei[0]
        p2 = ei[1]
        if p1[0] == p2[0]:
            xmin = p1[0] * size[0] * 2
            ymin = (min((p1[1], p2[1])) * 2 * size[1]) + size[1]
        elif p1[1] == p2[1]:
            xmin = (min((p1[0], p2[0])) * 2 * size[0]) + size[0]
            ymin = p1[1] * size[1] * 2
        for y in range(size[1]):
            for x in range(size[0]):
                gvl.append((x + xmin, y + ymin))
    
    buildGridGraph(g, gvl)
    return
