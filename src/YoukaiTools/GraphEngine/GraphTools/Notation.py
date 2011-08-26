def toVertexMathNotation(g):
   s = "{"
   for x in g.getVertexList():
      s = s + "v" + str(x) + ", "
   if g.getOrder() > 0: s = s[:-2]
   s += "}"
   return s

def toEdgeMathNotation(g):
   s = "{"
   for x in g.getEdgeList():
      ei = g.getEdgeInfo(x)
      st = ""
      if ei[2] == 0:  #if the edge is undirected
         st = st + "v" + str(ei[0]) + "v" + str(ei[1]) + ", "
      elif ei[2] == 1:
         st = st + "(v" + str(ei[0]) + ", v" + str(ei[1]) + "), "
      elif ei[2] == -1:
         st = st + "(v" + str(ei[1]) + ", v" + str(ei[0]) + "), "
      s = s + st
   if g.getEdgeNum() > 0: s = s[:-2]
   s += "}"
   return s

