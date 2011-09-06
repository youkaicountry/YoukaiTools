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

import collections

#FUNCTIONS THAT INVOLVE BUILDING AND MODIFYING BASIC GRAPHS

#takes an int specifying the number of vertices or an iterable containing the vertex names, and
#a list of the edges [(0, 1), (1, 2), (0, 2), (2, 4, 1)] (the third parameter, if given, is the order of a directed edge)
#with that, it clears and reconstructs the graph.
#TODO: make a directed version of this
def buildGraph(g, vertices, edges=None, vdata={}, edata={}):
    """
    @param g: The graph to write to.
    @type g: L{GraphEngine.BaseObjects.BaseGraph}
    @param vertices: A list of edges 
    
    """
    g.clearGraph()

    if isinstance(vertices, collections.Iterable):
        uvertices = vertices
    else:
        uvertices = range(vertices)
    
    for x in uvertices:
        g.addVertex(x)
    
    if edges is not None:
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

#Builds the graphs from dictionaries
#vertices should be either a number or a dictionary.
#If it is a number, then that many vertices will simply be added with
#integer ids.
#If it is a dictionary, then each entry is a vertex. There are 2 entries that are important:
#"data" and "name". "data" should be a dictionary of data entries attached to that vertex. "name" is
#the name of the vertex. if this is not present, then the dictionary key in vertices of that entry will
#be used.
#edges should be None or a dictionary. If None, then there will be no edges. If a dictionary. 
#then each entry will be an edge. #There are 4 important entries to each edge. "name", "vertices", "directed", and "data".
#"data" and "name" work the same as with vertices. "vertices" is a tuple containing the 2 vertices connected by
#the edge. "directed" should be True or False. If True, then it is directed from the first vertex in the "vertices" tuple
#to the second. You could also set "directed" to -1 to have it be directed from the second to the first.
def buildGraphD(g, vertices, edges=None):
    g.clearGraph()
    if not isinstance(vertices, collections.Iterable):
        o = {}
        for v in range(vertices):
            o[v] = {"name":v}
        vertices = o
        
    for key in vertices.keys():
        name = vertices[key]["name"] if "name" in vertices[key] else key
        datadic = vertices[key]["data"] if "data" in vertices[key] else None
        g.addVertex(name)
        if datadic is not None:
            for k in datadic.keys():
                g.setVertexData(name, k, datadic[k])
    
    if edges is not None:
        for key in edges.keys():
            name = edges[key]["name"] if "name" in edges[key] else key
            vertices = edges[key]["vertices"] 
            directed = edges[key]["directed"] if "directed" in edges[key] else 0
            datadic = edges[key]["data"] if "data" in edges[key] else None
            g.addEdge(vertices[0], vertices[1], directed, name)
            if datadic is not None:
                for k in datadic.keys():
                    g.setEdgeData(name, k, datadic[k])
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
   

