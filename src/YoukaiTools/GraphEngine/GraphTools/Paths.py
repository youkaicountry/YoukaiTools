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

import math
import heapq
import collections
from collections import deque

import YoukaiTools.PyRange.Paths as PyRangePaths

#FUNCTIONS THAT INVOLVE PATHS, PATHFINDING, AND CONNECTIVITY

#returns a list of all verticeprint(s that can be travelled to
def getReachableVertices(g, vertices):
    queue = deque(vertices)
    reachable = set(vertices)
    while len(queue) > 0:
        u = queue.popleft()
        c = g.getAdjacentVertices(u)
        for v in c:
            if v not in reachable:
                reachable.add(v)
                queue.append(v)
    return reachable

#returns list of all islands
def findAllIslands(g):
    outlist = []
    appendlist = []
    vl = g.getVertexList()
    for v in vl: #for each vertex in the list
        loc = len(outlist)
        inside = False
        for oi in range(len(outlist)):
            if v in outlist[oi]:
                loc = oi
                inside = True
                break
        if not inside:
            outlist.append(set([v]))

        for n in g.getAdjacentVertices(v):
            inside = False
            for oi in range(len(outlist)):
                if n in outlist[oi]:
                    if oi != loc:
                        appendlist.append(oi)
                        inside = True
                        break
            if not inside:
                if n not in outlist[loc]:
                    outlist[loc].add(n)
        for i in appendlist:
            if loc != i:
                for x in outlist[i]:
                    if x not in outlist[loc]:
                        outlist[loc].add(x)
        newout = []
        for oi in range(len(outlist)):
            if oi not in appendlist:
                newout.append(outlist[oi])
        outlist = list(newout)
        appendlist = []
        #print(outlist)
    return outlist

#given the graph and 2 vertices, returns a boolean representing whether
#there is a path from the start vertex to the end vertex
def hasPath(g, startvertex, endvertex):
    r = getReachableVertices(g, [startvertex])
    return endvertex in r

#Bellman-Ford Pathfinding
#Single source shortest path, allows negative weights, runs in O(vertices*edges) time
#returns a path tree
#source is the source vertex id
#weightdata is the weight data id on edges
def bellmanFordTree(g, source, costdata=None):
    vdic = __initSingleSourceVDic(g, source)
    for i in range(g.getOrder()-1):
        #print(i, vdic)
        for edge in g.getEdgeList():
            u, v, direction = g.getEdgeInfo(edge, True)
            dist = 1 if costdata is None else g.getEdgeData(edge, costdata)
            __relaxVertices(vdic, u, v, edge, dist)
            if direction == 0:
                __relaxVertices(vdic, v, u, edge, dist)
    return (source, vdic)

def hEuclidean2D(g, source, destination, xdata, ydata):
    dx = g.getVertexData(destination, xdata) - g.getVertexData(source, xdata)
    dy = g.getVertexData(destination, ydata) - g.getVertexData(source, ydata)
    return math.sqrt(dx*dx + dy*dy)

def hManhattan2D(g, source, destination, xdata, ydata):
    dx = g.getVertexData(destination, xdata) - g.getVertexData(source, xdata)
    dy = g.getVertexData(destination, ydata) - g.getVertexData(source, ydata)
    return abs(dx) + abs(dy)*1000

def AStarPath(g, source, destination, costdata=None, heuristic=hEuclidean2D, hparams=("x", "y")):
    vdic = {}
    Q = [(heuristic(g, source, destination, *hparams), 0, None, source)]
    heapq.heapify(Q)
    while(len(Q) != 0):
        h, d, e, v = heapq.heappop(Q)
        l = vdic.get(v)
        if l is not None and d >= l[0]: continue
        vdic[v] = [d, g.getEdgeEnd(v, e) if e is not None else None, e]
        if v == destination: break
        outbound = getOutbound(g, v)
        for ae, av in outbound:
            c = 1 if costdata is None else g.getEdgeData(ae, costdata)
            herecost = d + c
            bestcostav = vdic.get(av)
            if bestcostav is None or herecost <= bestcostav:
                heapq.heappush(Q, (herecost+heuristic(g, av, destination, *hparams), herecost, ae, av))
    return pathTree2Path((source, vdic), destination)

#destinations can be iterable to have multiple destinations to reach.
#if it isn't, then only one destination will be used and a non iterable path
#will be returned
def dijkstraPaths(g, source, destinations, costdata=None):
    it=True
    if not isinstance(destinations, collections.Iterable):
        destinations = [destinations]
        it=False
    vdic = {}
    remaining = set(destinations)
    Q = [(0, None, source)]
    heapq.heapify(Q)
    while(len(Q) != 0):
        d, e, v = heapq.heappop(Q)
        #if v in S: continue
        l = vdic.get(v)
        if l is not None and d >= l[0]: continue
        vdic[v] = [d, g.getEdgeEnd(v, e) if e is not None else None, e]
        if v in remaining:
            if len(remaining) == 1: break
            remaining.remove(v)
        outbound = getOutbound(g, v)
        for ae, av in outbound:
            c = 1 if costdata is None else g.getEdgeData(ae, costdata)
            herecost = d + c
            bestcostav = vdic.get(av)
            if bestcostav is None or herecost <= bestcostav:
                heapq.heappush(Q, (herecost, ae, av))
    out = []
    #print(vdic)
    for v in destinations:
        out.append(pathTree2Path((source, vdic), v))
    return out if it==True else out[0]

def dijkstraTree(g, source, costdata=None):
    vdic = {}
    Q = [(0, None, source)]
    heapq.heapify(Q)
    while(len(Q) != 0):
        d, e, v = heapq.heappop(Q)
        l = vdic.get(v)
        if l is not None and d >= l[0]: continue
        vdic[v] = [d, g.getEdgeEnd(v, e) if e is not None else None, e]
        outbound = getOutbound(g, v)
        for ae, av in outbound:
            c = 1 if costdata is None else g.getEdgeData(ae, costdata)
            herecost = d + c
            bestcostav = vdic.get(av)
            if bestcostav is None or herecost <= bestcostav:
                heapq.heappush(Q, (herecost, ae, av))
    return (source, vdic)

#returns a path from a given pathtree
#path = [ (vertex, nextedge), (vertex, nextedge), ... ]
def pathTree2Path(pathtree, destination):
    vdic = pathtree[1]
    out = []
    here = destination
    ne = None
    while(True):
        hv = here
        out.append((hv, ne))
        ne = vdic[here][2]
        if ne is None: break
        here = vdic[here][1]
    out.reverse()
    return out

def getReversePath(path):
    out = []
    for i, p in enumerate(path):
        opi = -(i+1)
        if i != len(path)-1:
            out.append((path[opi][0], path[opi-1][1]))
        else:
            out.append((path[opi][0], None))
    return out

def getOutboundEdges(g, vertexid):
    out = []
    for i in g.getAdjacentEdges(vertexid):
        ei = g.getEdgeInfo(i)
        if ei[2] == 0 : out.append(i)
        elif ei[0] == vertexid and ei[2] == 1 : out.append(i)
        elif ei[1] == vertexid and ei[2] == -1 : out.append(i)
    return out
      
def getOutboundVertices(g, vertexid):
    out = []
    oe = getOutboundEdges(g, vertexid)
    for edge in oe:
        out.append(g.getEdgeEnd(vertexid, edge))
    return out

def getOutbound(g, vertexid):
    out = []
    oe = getOutboundEdges(g, vertexid)
    for edge in oe:
        out.append((edge, g.getEdgeEnd(vertexid, edge)))
    return out

def getInboundEdges(g, vertexid):
    out = []
    for i in g.getAdjacentEdges(vertexid):
        ei = g.getEdgeInfo(i)
        if ei[2] == 0 : out.append(i)
        elif ei[1] == vertexid and ei[2] == 1 : out.append(i)
        elif ei[0] == vertexid and ei[2] == -1 : out.append(i)
    return out

def getInboundVertices(g, vertexid):
    out = []
    oe = getInboundEdges(g, vertexid)
    for edge in oe:
        out.append(g.getEdgeEnd(vertexid, edge))
    return

def getInbound(g, vertexid):
    out = []
    oe = getInboundEdges(g, vertexid)
    for edge in oe:
        out.append((edge, g.getEdgeEnd(vertexid, edge)))
    return

def getConnectingEdges(g, vertexid1, vertexid2, directed=False):
    out = []
    el = g.getAdjacentEdges(vertexid1)
    if not directed:
        for i in el:
            ei = g.getEdgeInfo(i)
            if ei[0] == vertexid2: out.append(i)
            elif ei[1] == vertexid2: out.append(i)
    else:
        for i in el:
            ei = g.getEdgeInfo(i)
            if ei[0] == vertexid2 and (ei[2] == 0 or ei[2] == -1): out.append(i)
            elif ei[1] == vertexid2 and (ei[2] == 0 or ei[2] == 1): out.apppend(i)
    return out

def makeSpatialPath2D(g, path, xdata='x', ydata='y'):
    cp = PyRangePaths.ContainerPath()
    for i, p in enumerate(path[:-1]):
        x0 = g.getVertexData(p[0], xdata)
        y0 = g.getVertexData(p[0], ydata)
        p2 = path[i+1][0]
        x1 = g.getVertexData(p2, xdata)
        y1 = g.getVertexData(p2, ydata)
        lp = PyRangePaths.LinePath(start=(x0, y0), end=(x1, y1))
        cp.addPiece(lp, (0,0))
    cp.update()
    return cp
#initializes a vdic
#[dist, lastvertex, lastedge]
def __initSingleSourceVDic(g, source):
    vdic = {}
    for v in g.getVertexList():
        vdic[v] = [0, None, None] if v == source else [float('inf'), None, None]
    return vdic

#vdic is the vertex dictionary
#u & v are the name of the vertices in vdic
#weight is the 
def __relaxVertices(vdic, u, v, edge, weight):
    add = (vdic[u][0] + weight) if vdic[u][0] != () else ()
    if vdic[v][0] > add:
        vdic[v][0] = add
        vdic[v][1] = u
        vdic[v][2] = edge
    return

