from YoukaiTools import GraphEngine
from YoukaiTools.GraphEngine.GraphTools.SpecialTypes import GridGraph
import random
import time

size = (6, 6)
recurse = 2

bg = GraphEngine.Graphs.BasicGraph()
GridGraph.buildGridGraph(bg, dimensions=size)
r = random.Random()

mt = time.time()
topmaze = GraphEngine.Graphs.BasicGraph()
GraphEngine.GraphTools.Span.recursiveBacktrack(bg, r=r, makegraph=topmaze)

last = topmaze
for n in range(recurse):
    bottommaze = GraphEngine.Graphs.BasicGraph()
    GridGraph.gridInGrid(bottommaze, last, size)
    bottommazefinal = GraphEngine.Graphs.BasicGraph()
    GraphEngine.GraphTools.Span.recursiveBacktrack(bottommaze, r=r, makegraph=bottommazefinal)
    last = bottommazefinal
print("Maze Generating Done. Took: " + str(time.time() - mt))

mt = time.time()
paths = GraphEngine.GraphTools.Paths.dijkstraPaths(bottommazefinal, (0, 0), [((size[0]**2)*2-size[0]-1, (size[1]**2)*2-size[0]-1)])
for path in paths:
    GraphEngine.GraphTools.Data.setDataToPath(bottommazefinal, path, vertexdata=("color", (0, 1, 0)), edgedata=("color", (0, 1, 0)))
print("Pathfinding Done. Took: " + str(time.time() - mt))

GraphEngine.Draw.drawSimple(bottommazefinal, "./output/multimaze.png", smallwidth=2048, layers=[("edge", ("color", (0, 0, 1.0))) ] )
