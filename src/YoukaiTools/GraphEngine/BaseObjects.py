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

"""
Base objects for GraphEngine.
"""

class BaseGraph(object):
    """
    The Base Graph object.
    """
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
        """
        Gets adjacent edges and vertices for the given vertex.
        @param vertexid: The id of the vertex.
        @return: A tuple containing (edge, vertex).
        @rtype: C{interable}
        """
        return
        
    def getVertexDataKeys(self, vertexid):
        """
        Gets all data keys from a given vertex.
        @param vertexid: The id of the vertex to get the data keys for.
        @return: A list of data keys.
        @rtype: C{iterable}
        """
        return
        
    def getVertexData(self, vertexid, index):
        """
        Retrieves the data associated with the given key.
        @param vertexid: The id of the vertex from which data will be retrieved.
        @param index: The key of the data to be retrieved.
        #return: The data associated with the key.
        """
        return

    def setVertexData(self, vertexid, index, data):
        """
        Attaches data to a vertex, under the given key.
        @param vertexid: The id of the vertex to which data will be set.
        @param index: The key to associate the data with.
        @param data: The data to attach to the vertex.
        """
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
        """
        Changes the id of an edge.
        @param edgeidold: The id of the edge to change.
        @param edgeidnew: The new id of the edge.
        """
        return
    
    def modifyEdge(self, edgeid, vertex1, vertex2, direction):
        """
        Modifies the attributes of the given edge.
        @param edgeid: The id of the edge to modify.
        @param vertex1: The id of the first vertex the edge connects.
        @param vertex2: The id of the second vertex the edge connects.
        @param direction: The direction of the edge.
        """
        return
    
    def removeEdge(self, edgeid):
        """
        Remove the given edge from the graph.
        @param edgeid: The id of the edge to remove.
        """
        return
        
    def getEdgeList(self):
        """
        Get a list of edges.
        @return: A list containing the id of each edge in the graph.
        @rtype: C{iterable}
        """
        return
        
    def getSize(self):
        """
        Returns the size (number of edges) of the graph.
        @return: The size of the graph.
        @rtype: C{int}
        """
        return
       
    def containsEdge(self, edgeid):
        """
        Checks whether the given edge id is in the graph.
        @param edgeid: The edge id to check for.
        @return: Whether or not the graph contains the edge.
        @rtype: C{bool}
        """
        return
    
    def getEdgeInfo(self, edgeid, normalize=False):
        """
        Gets the attributes of the given vertex.
        @param edgeid: The id of the edge for which to fetch data.
        @param normalize: Optional parameter that tells whether to normalize the order of the connected vertices by directedness.
        @type normalize: C{bool}
        @return: A tuple containing (vertex1, vertex2, directedness).
        @rtype: C{iterable}
        """
        return
    
    def getEdgeEnd(self, vertexid, edgeid):
        """
        For a given edge and vertex, finds the other vertex connected to the edge.
        @param vertexid: The id of the vertex.
        @param edgeid: The id of the edge.
        @return: The id of the other vertex.
        """
        return
        
    def getEdgeDataKeys(self, edgeid):
        """
        Gets all data keys from a given edge.
        @param edgeid: The id of the edge to get the data keys for.
        @return: A list of data keys.
        @rtype: C{iterable}
        """
        return
      
    def getEdgeData(self, edgeid, index):
        """
        Retrieves the data associated with the given key.
        @param edgeid: The id of the edge from which data will be retrieved.
        @param index: The key of the data to be retrieved.
        #return: The data associated with the key.
        """
        return

    def setEdgeData(self, edgeid, index, data):
        """
        Attaches data to a edge, under the given key.
        @param edgeid: The id of the edge to which data will be set.
        @param index: The key to associate the data with.
        @param data: The data to attach to the edge.
        """
        return
    
