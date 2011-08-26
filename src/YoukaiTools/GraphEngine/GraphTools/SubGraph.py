from .. import Graphs
import Paths
from collections import deque

def makeHistoryGraphs(g, history, graphtype=Graphs.BasicGraph, graphtypeinit=(), entries=None):
    out = {}
    if entries is None:
        entries = history.keys()
    for ent in entries:
        newg = graphtype(*graphtypeinit)
        copyGraph(newg, g)
        for v in history[ent]:
            #print(v)
            for k in history[ent][v]:
                newg.setVertexData(v, k, history[ent][v][k])
        out[ent] = newg
    return out

#copy cg into g
def copyGraph(g, cg, vertexlist=None, copyvdata=True, edgelist=None, copyedata=True):
    if vertexlist is None:
        vertexlist = cg.getVertexList()
    if edgelist is None:
        edgelist = cg.getEdgeList()
    for v in vertexlist:
        copyVertex(g, cg, v, copyvdata)
    for e in edgelist:
        copyEdge(g, cg, e, False, copyedata)
    return

def copyVertex(g, cg, v, copydata=True):
    if not g.containsVertex(v):
        g.addVertex(v)
    if copydata:
        for vd in cg.getVertexDataKeys(v):
            g.setVertexData(v, vd, cg.getVertexData(v, vd))
    return

def copyEdge(g, cg, e, copyvdata=True, copyedata=True):
    v1, v2, d = cg.getEdgeInfo(e)
    copyVertex(g, cg, v1, copyvdata)
    copyVertex(g, cg, v2, copyvdata)
    if not g.containsEdge(e):
        g.addEdge(v1, v2, d, e)
    if copyedata:
        for ed in cg.getEdgeDataKeys(e):
            g.setEdgeData(e, ed, cg.getEdgeData(e, ed))
    return

#graph reduction for graphs whose important vertices are the ones with
#junctionscorridorGraphReduction
#Only use this on an undirected graph
def corridorGraphReduction(g, rg, cost=None, outcost="cost", edataname="edata", pathname = "path", reversepathname="reversepath"):
    vset = set()
    eset = set()
    equeue = deque()
    #first find all vertices with order =1 or >2
    for v in g.getVertexList():
        ae = g.getAdjacentEdges(v)
        o = len(ae)
        if o == 1 or o > 2:
            #add it to the set and the new graph
            vset.add(v)
            rg.addVertex(v)
            for key in g.getVertexDataKeys(v):
                    rg.setVertexData(v, key, g.getVertexData(v, key))
            #put properties here
            for e in ae:
                equeue.append(e)
    while (len(equeue) > 0):
        e = equeue.popleft()
        if e in eset: continue
        ce = e
        ei = g.getEdgeInfo(ce)
        fromv = ei[0] if ei[0] in vset else ei[1]
        startv = fromv
        add = 0
        datae = {}
        path = []
        #follow the current path
        while True:
            if outcost is not None: 
                effc = 1 if cost is None else g.getEdgeData(ce, cost)
                add += effc
            if pathname is not None: path.append((fromv, ce))
            if edataname is not None: 
                datae[ce] = {}
                for key in g.getEdgeDataKeys(ce):
                    datae[ce][key] = g.getEdgeData(ce, key)
            tov = g.getEdgeEnd(fromv, ce)
            if tov in vset:
                eset.add(ce)            #get the other edge on tov and
                addede = rg.addEdge(startv, tov)
                if outcost is not None: rg.setEdgeData(addede, outcost, add)
                if edataname is not None: rg.setEdgeData(addede, edataname, datae)
                if pathname is not None:
                    path.append((tov, None))
                    rg.setEdgeData(addede, pathname, path)
                    if reversepathname is not None: rg.setEdgeData(addede, reversepathname, Paths.getReversePath(path))
                break
            #get the other edge on tov and set ce and fromv
            ae = g.getAdjacentEdges(tov)
            ne = None
            for e in ae:
                if ce != e: ne = e; break
            ce = ne
            fromv = tov
    return
