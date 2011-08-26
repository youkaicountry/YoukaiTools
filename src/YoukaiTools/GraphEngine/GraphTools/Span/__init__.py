import YoukaiTools.GraphEngine

from collections import deque
import heapq
from . import Worms

#set r to an instance of Random to have a random maze
#set r to None to have it be normal Kruskal's algorithm
def kruskal(g, cost=None, r=None, makegraph=None):
    out = []
    wall_list = []
    for e in g.getEdgeList():
        c = 1 if cost is None else g.getEdgeData(e, cost)
        wall_list.append((c, e))
    if r is None:
        wall_list.sort()
    else:
        r.shuffle(wall_list)
    vid = {}
    id_list = []
    for i, v in enumerate(g.getVertexList()):
        vid[v] = i
        id_list.append([v])
    for wall in wall_list:
        v1, v2, d = g.getEdgeInfo(wall[1])
        id1 = vid[v1]
        id2 = vid[v2]
        if id1 != id2:
            out.append(wall[1])
            for v in id_list[id2]:
                id_list[id1].append(v)
                vid[v] = id1
            id_list[id2] = []
    if makegraph is not None:
        GraphEngine.GraphTools.SubGraph.copyGraph(makegraph, g, edgelist=out)
    return out

def recursiveBacktrack(g, cost=None, r=None, start=None, makegraph=None):
    if start is None:
        start = g.getVertexList()[0]
    out = []
    found = set()
    #path = [start]
    path = deque()
    path.append(start)
    nv = start
    while len(path) > 0:
        found.add(nv) #add the vertex to found list
        n = g.getAdjacent(nv)  #get adjacent
        realn = []                    
        for o in n:                    #reduce to neighbors that have not been found
            if o[1] not in found:
                c = 1 if cost is None else g.getEdgeData(o[0], cost)
                realn.append((c, o[0], o[1]))
        if len(realn) > 0:             #check if there are any unfound neighbors
            path.append(nv)            #append here to the path
            choice = realn[r.randint(0, len(realn)-1)] if r is not None else min(realn)
            if choice[2] not in found: #remove this?
                out.append(choice[1])
                nv = choice[2]
                continue #remove?
        else:
            if len(path) == 0: break 
            #a = path.pop(len(path)-1) #use a deque?
            a = path.pop()
            nv = a
            continue #remove
    if makegraph is not None:
        YoukaiTools.GraphEngine.GraphTools.SubGraph.copyGraph(makegraph, g, edgelist=out)
    return out

def prim(g, cost=None, r=None, start=None, makegraph=None):
    if start is None:
        start = g.getVertexList()[0]
    visited = set()
    visited.add(start)
    out = []
    a = g.getAdjacent(start)
    for o in a:
        adj = []
        c = 1 if cost is None else g.getEdgeData(o[0], cost)
        adj.append((c, o[0], o[1]))
        if r is None: heapq.heapify(adj)
    while len(adj) > 0:
        #pick next edge to check
        if r is None:
            ne = heapq.heappop(adj)
        else:
            v = r.randint(0, len(adj)-1)
            ne = adj.pop(v)
        nv = ne[2]
        if nv in visited: continue
        visited.add(nv)
        out.append(ne[1])
        a = g.getAdjacent(nv)
        for o in a:
            if a[1] not in visited:
                c = 1 if cost is None else g.getEdgeData(o[0], cost)
                if r is not None:
                    heapq.heappush(adj, (c, o[0], o[1]))
                else:
                    adj.append((c, o[0], o[1]))
    if makegraph is not None:
        YoukaiTools.GraphEngine.GraphTools.SubGraph.copyGraph(makegraph, g, edgelist=out)
    return out
