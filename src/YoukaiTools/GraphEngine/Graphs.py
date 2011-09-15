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

from . import BaseObjects

class BasicGraph(BaseObjects.BaseGraph):
    def __init__(self):
        self.clearGraph()

    def clearGraph(self):
        self.vertices = {}
        self.edges = {}
        self.vertextop = 0
        self.edgetop = 0

    def addVertex(self, vertexid=None):
        #the list is: connected vertices, connected edges, and data
        if (vertexid is None): 
            usev = self.vertextop
            self.vertextop += 1
        else:
            usev = vertexid
        self.vertices[usev] = [set(), set(), {}]
        out = self.vertextop
        return usev
  
    def renameVertex(self, vertexidold, vertexidnew):
        a = self.vertices[vertexidold]
        del self.vertices[vertexidold]
        self.vertices[vertexidnew] = a
        for v in self.vertices.keys():
            if vertexidold in self.vertices[v][0]:
                self.vertices[v][0].remove(vertexidold)
                self.vertices[v][0].add(vertexidnew)
        for e in self.edges.keys():
            if self.edges[e][0][0] == vertexidold:
                self.edges[e][0][0] = vertexidnew
            if self.edges[e][0][1] == vertexidold:
                self.edges[e][0][1] = vertexidnew
        return

    def addEdge(self, vertex1, vertex2, direction=0, edgeid=None):
        #the list is: connection info, and data
        if (edgeid is None): 
            usev = self.edgetop
            self.edgetop += 1
        else:
            usev = edgeid
        self.__makeedgeinfo(vertex1, vertex2, direction, usev)
        return usev
      
    def containsVertex(self, vertexid):
        return vertexid in self.vertices
       
    def containsEdge(self, edgeid):
        return edgeid in self.edges
   
    #get vertices that connect this one
    #was getConnections
    def getAdjacentVertices(self, vertexid):
        return [x for x in self.vertices[vertexid][0]]
   
    #get all edges connected to a vertex
    #was getVertexEdges   
    def getAdjacentEdges(self, vertexid):
        return [x for x in self.vertices[vertexid][1]]
   
    #return [(egdeid, vertexid), ...] for all adjacent connections
    def getAdjacent(self, vertexid):
        #return [(x[1], x[0]) for x in self.vertices[vertexid]]
        return [(e, (self.getEdgeEnd(vertexid, e))) for e in self.vertices[vertexid][1]]

    def getVertexData(self, vertexid, index):
        return self.vertices[vertexid][2][index]

    def setVertexData(self, vertexid, index, data):
        self.vertices[vertexid][2][index] = data
        return

    def getEdgeData(self, edgeid, index):
        return self.edges[edgeid][1][index]

    def setEdgeData(self, edgeid, index, data):
        self.edges[edgeid][1][index] = data
        return

    def removeVertex(self, vertexid):
        l = [x for x in self.vertices[vertexid][1]]
        for x in l:
            print("ll:" + str(x))
            self.removeEdge(x)
        del self.vertices[vertexid]
        return

    def removeEdge(self, edgeid):
        self.__clearedgeinfo(self.edges[edgeid][0][0], edgeid)
        self.__clearedgeinfo(self.edges[edgeid][0][1], edgeid)
        del self.edges[edgeid]
        return

    def modifyEdge(self, edgeid, vertex1, vertex2, direction=0):
        oldv1 = self.edges[edgeid][0][0]
        oldv2 = self.edges[edgeid][0][1]
        self.__clearedgeinfo(oldv1, edgeid)
        self.__clearedgeinfo(oldv2, edgeid)
        self.__makeedgeinfo(vertex1, vertex2, direction, edgeid)
        return

    def __makeedgeinfo(self, vertex1, vertex2, direction, edgeid):
        self.edges[edgeid] = [[vertex1, vertex2, direction], {}]
        #add the connection information to the vertices
        if direction == 0:
            self.vertices[vertex1][0].add(vertex2)
            self.vertices[vertex1][1].add(edgeid)
            self.vertices[vertex2][0].add(vertex1)
            self.vertices[vertex2][1].add(edgeid)
        elif direction == 1:
            self.vertices[vertex1][0].add(vertex2)
            self.vertices[vertex1][1].add(edgeid)
            self.vertices[vertex2][1].add(edgeid)
        elif direction == -1:
            self.vertices[vertex1][1].add(edgeid)
            self.vertices[vertex2][0].add(vertex1)
            self.vertices[vertex2][1].add(edgeid)

    def __clearedgeinfo(self, vertexid, edgeid):
        self.vertices[vertexid][1].remove(edgeid)
        v1 = self.edges[edgeid][0][0]
        v2 = self.edges[edgeid][0][1]
        v = -1
        if v1 == vertexid: v = v2
        if v2 == vertexid: v = v1
        vtest = False
        for x in self.vertices[vertexid][1]:
            if self.__isconnected(vertexid, v, x):
                vtest = True
        if not vtest:
            try:
                self.vertices[vertexid][0].remove(v)
            except:
                pass
        return

    def __isconnected(self, sourcev, targetv, edgeid):
        if self.edges[edgeid][0][2] == 0:
            if self.edges[edgeid][0][0] == sourcev:
                if self.edges[edgeid][0][1] == targetv:
                    return True
            if self.edges[edgeid][0][0] == targetv:
                if self.edges[edgeid][0][1] == sourcev:
                    return True
        if self.edges[edgeid][0][2] == 1:
            if self.edges[edgeid][0][0] == sourcev:
                if self.edges[edgeid][0][1] == targetv:
                    return True
        if self.edges[edgeid][0][2] == -1:
            if self.edges[edgeid][0][0] == targetv:
                if self.edges[edgeid][0][1] == sourcev:
                    return True
        return False

    def getVertexDataKeys(self, vertexid):
        return [x for x in self.vertices[vertexid][2].keys()]
      
    def getEdgeDataKeys(self, edgeid):
        return [x for x in self.edges[edgeid][1]]

    #should return a list (vertex1, vertex2, direction)
    def getEdgeInfo(self, edgeid, normalized=False):
        v1, v2, d = self.edges[edgeid][0]
        if normalized:
            if (d == 1) or d == 0:
                return (v1, v2, d)
            return (v2, v1, 1)
        else:
            return (v1, v2, d)

    def getVertexList(self):
        return self.vertices.keys()

    def getEdgeList(self):
        return self.edges.keys()
     
    def getOrder(self):
        return len(self.vertices)
   
    def getSize(self):
        return len(self.edges)
   
    def getEdgeEnd(self, vertexid, edgeid):
        ei = self.edges[edgeid][0]
        if ei[0] == vertexid: return ei[1]
        else: return ei[0]

