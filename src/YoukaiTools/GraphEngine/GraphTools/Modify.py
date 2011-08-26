#makes all edges direction be either 0 or 1 (reverses -1 order)
def normalizeEdges(g):
   for x in g.getEdgeList():
      ei = g.getEdgeInfo(x)
      if ei[2] == -1:
         g.modifyEdge(x, ei[1], ei[0], 1)
   return
