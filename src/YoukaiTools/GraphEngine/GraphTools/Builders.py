#FUNCTIONS THAT INVOLVE BUILDING AND MODIFYING BASIC GRAPHS

#have buildgraph accept list instead of just ints

#takes an int specifying the number of vertices, and
#a list of the edges [(0, 1), (1, 2), (0, 2), (2, 4, 1)] (the third parameter, if given, is the order of a directed edge)
#with that, it clears and reconstructs the graph.
#TODO: make a directed version of this
def buildGraph(g, vertices, edges, vdata={}, edata={}):
    """
    @param g: The graph to write to.
    @type g: L{GraphEngine.BaseObjects.BaseGraph}
    @param vertices: A list of edges 
    
    """
    g.clearGraph()
    
    for x in range(vertices):
        g.addVertex()
    
    for x in edges:
        l = 0
        if len(x) >= 3:
            l = x[2]       
        e = g.addEdge(x[0], x[1], l)
        if len(x) == 4:
            for i in x[3]:
                g.setEdgeData(e, i[0], i[1])
    
    #print(vdata)   
    for vd in vdata.keys():
        for i in vdata[vd]:
            #print(str(vd) + " " + str(i[0]) + " " + str(i[1]))
            g.setVertexData(vd, i[0], i[1])
   
    for ed in edata.keys():
        for i in edata[ed]:
            g.setEdgeData(ed, i[0], i[1])
   
    return



#appends g2 and all of its properties to g. Returns the first vertex id and the first edge id
def appendGraph(g, g2):
   #get and sort the vertex lists
   vl = [x for x in g2.getVertexList()]
   vl.sort()
   el = [x for x in g2.getEdgeList()]
   el.sort()
   
   vstart = g.getOrder()
   estart = g.getSize()
   
   #setup the new vertices
   for i in vl:
      n = g.addVertex()
      for di in g2.getVertexDataKeys(i):
         g.setVertexData(n, di, g2.getVertexData(i, di))
   
   v2ne = {}
   for i in range(len(el)):
      v2ne[el[i]] = i
   #set up the new edges
   for i in el:
      edgeinfo = g2.getEdgeInfo(i)
      n = g.addEdge(v2ne[edgeinfo[0]]+vstart, v2ne[edgeinfo[1]]+vstart, edgeinfo[2])
      for di in g2.getEdgeDataKeys(i):
         g.setEdgeData(n, di, g2.getEdgeData(i, di))
   return (vstart, estart)
   

