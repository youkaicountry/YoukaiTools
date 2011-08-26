from YoukaiTools import GraphEngine

'''
Created on May 2, 2011

@author: nathan
'''

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
