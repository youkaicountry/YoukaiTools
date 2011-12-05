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

class BaseGraph(object):
    def __init__(self):
        return
    
    #VERTEX METHODS
    def addVertex(self, vertexid=None):
        """
        Adds a new vertex to the graph.
        @param vertexid: The id to use for identifying the vertex. If None, an id will be automatically generated.
        @return: The id of the newly created vertex.
        """
        return
    
    def renameVertex(self, vertexidold, vertexidnew):
        """
        Changes the id of a vertex.
        @param vertexidold: The id of the vertex to change.
        @param vertexidnew: The new id of the vertex.
        """
        return
       
    def removeVertex(self, vertexid):
        """
        Remove the given vertex from the graph.
        @param vertexid: The id of the vertex to remove.
        """
        return
        
    def getVertexList(self):
        """
        Get a list of vertices.
        @return: A list containing the id of each vertex in the graph.
        """
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
        """
        Finds all vertices adjacent to the given vertex. Does not take into account directedness.
        @param vertexid: The id of the vertex.
        @return: A list of the ids of vertices adjacent to the given vertex.
        """
        return
        
    def getAdjacentEdges(self, vertexid):
        """
        Finds all edges adjacent to the given vertex. Does not take into account directedness.
        @param vertexid: The id of the vertex.
        @return: A list of the ids of edges adjacent to the given vertex.
        """
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
    
