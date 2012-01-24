import random

import YoukaiTools.GraphEngine as GraphEngine

r = random.Random(11460)

bg = GraphEngine.BasicGraph()
for i in xrange(100000):
    print("iter " + str(i))
    num = r.randint(0,3)
    if num == 0:
        bg.addVertex()
    if num == 1:
        if bg.getOrder() > 1:
            vertices = bg.getVertexList()
            r.shuffle(vertices)
            bg.addEdge(vertices[0], vertices[1])
    if num == 2:
        if bg.getOrder() > 0:
            vertices = bg.getVertexList()
            r.shuffle(vertices)
            bg.removeVertex(vertices[0])
    if num == 3:
        if bg.getSize() > 1:
            edges = bg.getEdgeList()
            r.shuffle(edges)
            bg.removeEdge(edges[0])
    if bg.getSize() > 1:
        
        for vertex in bg.getVertexList():
            edges = bg.getAdjacentEdges(vertex)
            if len(edges) > 0:
                for edge in edges:
                    print(bg.getEdgeEnd(vertex, edge))
        
    
"""
bg = GraphEngine.BasicGraph()
a = bg.addVertex(1)
b = bg.addVertex(1)
c = bg.addVertex(1)
d = bg.addVertex(1)
print(a,b,c,d)
e1 = bg.addEdge(a, c)
e2 = bg.addEdge(a, c)
e3 = bg.addEdge(a, c)
bg.removeEdge(e2)
e4 = bg.addEdge(c,d)
print(e1, e2, e3, e4)

bg.getEdgeEnd(c, e3)
ed = bg.getAdjacentEdges(c)
for edge in ed:
    bg.getEdgeEnd(c, edge)

bg.removeEdge(e4)
bg.removeEdge(e1)
bg.getAdjacent(c)
"""
