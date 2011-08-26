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
