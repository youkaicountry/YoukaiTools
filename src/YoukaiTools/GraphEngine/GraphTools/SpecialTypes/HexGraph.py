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
