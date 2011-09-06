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
from YoukaiTools.GraphEngine.GraphTools.SpecialTypes import AdjacencyGraph
import random

size = 6

gg = AdjacencyGraph.GridGraph()
l = GraphEngine.GraphTools.Regions.expandFromVertex(gg, [(0, 0)], size)
#print(gg.getAdjacent((0, 0)))
bg = GraphEngine.Graphs.BasicGraph()
GraphEngine.GraphTools.SubGraph.copyGraph(bg, gg, vertexlist=l[1], edgelist=l[0])

hg = AdjacencyGraph.HexGraph()
l = GraphEngine.GraphTools.Regions.expandFromVertex(hg, [(0, 0)], size)
#print(gg.getAdjacent((0, 0)))
bg2 = GraphEngine.Graphs.BasicGraph()
GraphEngine.GraphTools.SubGraph.copyGraph(bg2, hg, vertexlist=l[1], edgelist=l[0])

GraphEngine.Draw.drawSimple(bg, "./output/expanded_grid.png", smallwidth=512, layers=[("vertex", .007, ("color", (.5, 0, 0))), ("edge", ("color", (0, 0, 1.0)))] )
GraphEngine.Draw.drawSimple(bg2, "./output/expanded_hex.png", smallwidth=512, layers=[("vertex", .007, ("color", (.5, 0, 0))), ("edge", ("color", (0, 0, 1.0)))] )

r = random.Random()
mazeg = GraphEngine.Graphs.BasicGraph()
edges = GraphEngine.GraphTools.Span.prim(bg2, r=r, makegraph=mazeg)
paths = GraphEngine.GraphTools.Paths.dijkstraPaths(mazeg, (0, 1), [(1, 1)])
for path in paths:
    GraphEngine.GraphTools.Data.setDataToPath(mazeg, path, vertexdata=("color", (0, 1, 0)), edgedata=("color", (0, 1, 0)))
GraphEngine.Draw.drawSimple(mazeg, "./output/hex_maze.png", smallwidth=512, layers=[("vertex", .002, ("color", (.5, 0, 0))), ("edge", ("color", (0, 0, 1.0)))] )
