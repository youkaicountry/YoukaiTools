class BaseGraph(object):
    def __init__(self):
       return
    
    #VERTEX METHODS
    def addVertex(self, vertexid=None):
       """
       Adds a new vertex to the graph.
       @param vertexid: The id to use for the vertex. If None, an id will be automatically generated.
       @return: The id of the newly created vertex.
       """
       return
    
    def renameVertex(self, vertexidold, vertexidnew):
        return
       
    def removeVertex(self, vertexid):
        return
        
    def getVertexList(self):
        return
        
    def getOrder(self):
       """
       Returns the order (number of vertices) of the graph.
       @return: The order of the Graph.
       @rtype: C{int}
       """
       return
   
    def containsVertex(self, vertexid):
       """
       Checks whether the given vertex id is in the graph.
       @param vertexid: The vertex id to check for.
       @return: Whether or not the graph contains the vertex.
       @rtype: C{bool}
       """
       return
       
    def getAdjacentVertices(self, vertexid):
        return
        
    def getAdjacentEdges(self, vertexid):
        return
    
    def getAdjacent(self, vertexid):
        return
        
    def getVertexDataKeys(self, vertexid):
        return
        
    def getVertexData(self, vertexid, index):
        return

    def setVertexData(self, vertexid, index, data):
        return
    
    #EDGE METHODS
    def addEdge(self, vertex1, vertex2, direction=0, edgeid=None):
       """
       Adds a new edge to the graph.
       @param vertex1: The id of the first vertex the edge connects.
       @param vertex2: The id of the second vertex the edge connects.
       @param direction: If 0, the edge is undirected. If 1, the edge is directed vertex1->vertex2. If -1, the edge is directed vertex2->vertex1.
       @param edgeid: The id to use for the edge.
       @return: The id of the newly created edge.
       """
       return
    
    def renameEdge(self, edgeidold, edgeidnew):
        return
    
    def modifyEdge(self, edgeid, vertex1, vertex2, direction):
        return
    
    def removeEdge(self, edgeid):
        return
        
    def getEdgeList(self):
        return
        
    def getSize(self):
       """
       Returns the size (number of edges) of the graph.
       @return: The size of the graph.
       @rtype: C{int}
       """
       return
       
    def containsEdge(self, edgeid):
        return
    
    #should return a list (vertex1, vertex2, direction)
    def getEdgeInfo(self, edgeid, normalize=False):
        return
    
    def getEdgeEnd(self, vertexid, edgeid):
        return
        
    def getEdgeDataKeys(self, edgeid):
        return
      
    def getEdgeData(self, edgeid, index):
        return

    def setEdgeData(self, edgeid, index, data):
        return
    

      


