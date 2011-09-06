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

#FUNCTIONS THAT INVOLVE BREAKING UP A GRAPH INTO LOGICAL REGIONS

#regionsize = 0 - 1.0 determining chance of keepin a region the same size
#coherency = 0 - 1.0 determining chance of regions being broken up
#startvertex = the vertex number to start from
#random = a random object
#regions = the number of regions. Set this to None or < 0 to get the normalize 0.0 - 1.0
#leveldataindex = what data index to shove the level data into
def setLevels(g, random, startvertex, coherency, regionsize,  regions, leveldataindex):
   #set all levels
   queue = [startvertex]
   neighbors = []
   for v in g.getVertexList():
      g.setVertexData(v, leveldataindex, -1)
   last = -1
   #regionsize = 0
   while len(queue) > 0:
      here = queue.pop(0)
      random.shuffle(queue)
      for n in g.getConnections(here):
         if g.getVertexData(n, leveldataindex) == -1:
            neighbors.append(n)
      random.shuffle(neighbors)
      stay = (random.random() < coherency) and (len(neighbors) > 0) #pick from neighbors?
      if stay:
         queue.insert(0, neighbors.pop(0))
      queue = queue + neighbors
      neighbors = []
      if last == -1:
         last = 0
      else:
         if random.random() > regionsize:
            last += 1
      g.setVertexData(here, leveldataindex, last)
      
   #now last is the highest. Normalize everything from 0.0 - 1.0
   last = float(last)
   for v in g.getVertexList():
      g.setVertexData(v, leveldataindex, (float(g.getVertexData(v, leveldataindex)) / last))
      if regions != None and regions > 0:
         g.setVertexData(v, leveldataindex, int(regions*(float(g.getVertexData(v, leveldataindex)))))

   return
   
#calculates regions
def findGeometryRegions(g):
    regionnum = {}   #vertex to regionnum (use for marking)
    regionlist = []  #regionnum to vertex
    marked = 0       #number of marked vertices
    nextvertex = 0   #next vertex to start with
    while marked < g.getVertexNum():
        pass #do the stuff here.
        #pick a vertex
        #spread until criteria is met
        #advance regionnum one, pick new region
    return

#returns list of vertices and edges
def expandFromVertex(g, starts, levels):
    border = []
    bordern = []
    border.extend(starts)
    edges = set()
    vertices = set()
    for i in range(levels):
        for v in border:
            vertices.add(v)
            adj = g.getAdjacent(v)
            for a in adj:
                if a[1] not in vertices:
                    bordern.append(a[1])
                    vertices.add(a[1])
                edges.add(a[0])
        border = bordern
        bordern = []
    #finish up edges on border vertices
    for v in border:
        adj = g.getAdjacent(v)
        for a in adj:
            if a[1] in vertices:
                edges.add(a[0])
    return (edges, vertices)

