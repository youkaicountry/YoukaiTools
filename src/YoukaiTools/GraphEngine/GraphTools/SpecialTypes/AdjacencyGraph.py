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

from YoukaiTools import GraphEngine

class BaseAdjacencyGraph(GraphEngine.BaseObjects.BaseGraph):
    def __init__(self):
        self.modified_vertices = set()
        self.modified_edges = set()
        self.mod_graph = None
        self.vertex_data = {}
        self.edge_data = {}
        self.modified_vertex_name = {}
        self.modified_edge_name = {}
        self.coords = {"x": 0, "y": 1, "z": 2}
        return
    
    #override
    def getInfiniteAdjacent(self, vertexid):
        return
    
    #override... return a dic
    def getInfiniteCoordinate(self, vertexid, coordnum):
        return
    
    #override
    #set self.coords to a set of coords
    def nameCoordinates(self, coords):
        self.coords = {}
        for i, c in enumerate(coords):
            self.coords[c] = i
        return
    
    def getAdjacent(self, vertexid):
        if vertexid not in self.modified_vertices:
            return self.getInfiniteAdjacent(vertexid)
        else:
            return self.mod_graph.getAdjacent(vertexid)
        return
    
    #override
    def containsVertex(self, vertexid):
        return
    
    def __getEdgeName(self, edgeid):
        v = self.modified_edge_name.get(edgeid)
        if v is not None:
            return self.modified_edge_name[edgeid]
        return edgeid
    
    def __getVertexName(self, vertexid):
        v = self.modified_vertex_name.get(vertexid)
        if v is not None:
            return self.modified_vertex_name[vertexid]
        return vertexid
    
    def getAdjacentVertices(self, vertexid):
        return [x[1] for x in self.getAdjacent(vertexid)]
    
    def getAdjacentEdges(self, vertexid):
        return [x[0] for x in self.getAdjacent(vertexid)]
    
    def getVertexData(self, vertexid, index):
        if index in self.coords:
            if index not in self.vertex_data: 
                return self.getInfiniteCoordinate(vertexid, self.coords[index])
        return self.vertex_data[vertexid][index]
    
    def getVertexDataKeys(self, vertexid):
        print self.vertex_data.keys() + self.coords.keys()
        return self.vertex_data.keys() + self.coords.keys()
    
    def getEdgeDataKeys(self, edgeid):
        return self.edge_data.keys()

    def setVertexData(self, vertexid, index, data):
        if vertexid not in self.vertex_data:
            self.vertex_data[vertexid] = {}
        self.vertex_data[vertexid] = data
        return

    def getEdgeData(self, edgeid, index):
        return self.edge_data[edgeid][index]
    
    def getEdgeInfo(self, edgeid):
        return (edgeid[0], edgeid[1], 1)
    
    def setEdgeData(self, edgeid, index, data):
        if edgeid not in self.edge_data:
            self.edge_data[edgeid] = {}
        self.edge_data[edgeid] = data
        return

class GridGraph(BaseAdjacencyGraph):
    def __init__(self):
        BaseAdjacencyGraph.__init__(self)
        self.nameCoordinates(["x", "y"])
        #super(GridGraph, self)
        return
    
    def getInfiniteCoordinate(self, vertexid, coordnum):
        return vertexid[coordnum]
    
    def getInfiniteAdjacent(self, vertexid):
        out = []
        vl = [(vertexid[0]-1, vertexid[1]), (vertexid[0]+1, vertexid[1]), (vertexid[0], vertexid[1]-1), (vertexid[0], vertexid[1]+1)]
        for v in vl:
            out.append(((min([vertexid, v]), max([vertexid, v])), v))
        return out
    
    def containsVertex(self, vertexid):
        if len(vertexid) != 2: return False
        try:
            self.__getAdjacent(vertexid)
        except Exception:
            return False
        return True
    
class HexGraph(BaseAdjacencyGraph):
    def __init__(self):
        BaseAdjacencyGraph.__init__(self)
        self.nameCoordinates(["x", "y"])
        #super(GridGraph, self)
        return
    
    def getInfiniteCoordinate(self, vertexid, coordnum):
        if coordnum == 1:
            if abs(vertexid[0]) % 2 == 1:
                return vertexid[coordnum] + .5
        return vertexid[coordnum]
    
    def getInfiniteAdjacent(self, vertexid):
        out = []
        vl = [(vertexid[0]-1, vertexid[1]), (vertexid[0]+1, vertexid[1]), (vertexid[0], vertexid[1]-1), (vertexid[0], vertexid[1]+1)]
        if vertexid[0] % 2 == 1:
            vl.append( (vertexid[0]-1, vertexid[1]+1) )
            vl.append( (vertexid[0]+1, vertexid[1]+1) )
        else:
            vl.append( (vertexid[0]-1, vertexid[1]-1) )
            vl.append( (vertexid[0]+1, vertexid[1]-1) )
        for v in vl:
            out.append(((min([vertexid, v]), max([vertexid, v])), v))
        return out
    
    def containsVertex(self, vertexid):
        if len(vertexid) != 2: return False
        try:
            self.__getAdjacent(vertexid)
        except Exception:
            return False
        return True