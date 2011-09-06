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

from YoukaiTools import GraphEngine

def displayGraph(g):
    for x in g.getVertexList():
        print("V"+str(x)+":")
        print("Connections: "+str(g.getAdjacentEdges(x)))

bg = GraphEngine.BasicGraph()

v = 16
e = [(8, 4), (6, 4, 1), (4, 0, -1), (2, 3), (2, 10, 1), (3, 10), (11, 15), (15, 1, -1), (1, 5), (5, 7), (5, 9, -1), (1, 12, 1), (14, 12, 1)]

GraphEngine.GraphTools.Builders.buildGraph(bg, v, e)

displayGraph(bg)
bg.renameVertex(12, "hello")
displayGraph(bg)
