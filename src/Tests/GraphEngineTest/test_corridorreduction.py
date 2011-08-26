from YoukaiTools import GraphEngine
from YoukaiTools.GraphEngine.GraphTools.SpecialTypes import GridGraph
from YoukaiTools.MazeGen.generators import maze as maze
import random

size = (16, 16)

bg = GraphEngine.Graphs.BasicGraph()
GridGraph.buildGridGraph(bg, dimensions=size)
outg = GraphEngine.Graphs.BasicGraph()
r = random.Random()
GraphEngine.GraphTools.Span.recursiveBacktrack(bg, r=r, makegraph=outg)

rg = GraphEngine.BasicGraph()
GraphEngine.GraphTools.SubGraph.corridorGraphReduction(outg, rg, reversepathname="reversepath")

#pathsm = GraphEngine.GraphTools.Paths.dijkstraPaths(bg, (0, 0), [(size[0]-1, size[1]-1)])
#for path in pathsm:
#    GraphEngine.GraphTools.Data.setDataToPath(bg, path, vertexdata=("color", (0, 1, 0)), edgedata=("color", (0, 1, 0)))

#pathsr = GraphEngine.GraphTools.Paths.dijkstraPaths(rg, (0, 0), [(size[0]-1, size[1]-1)])
#for path in pathsr:
#    GraphEngine.GraphTools.Data.setDataToPath(rg, path, vertexdata=("color", (0, 1, 0)), edgedata=("color", (0, 1, 0)))

GraphEngine.Draw.drawSimple(outg, "./output/maze_before_reduce.png", smallwidth=512, layers=[("edge", ("color", (0, 0, 1.0))), ("vertex", .007, ("color", (1.0, 0, 0)))] )
GraphEngine.Draw.drawSimple(rg, "./output/maze_after_reduce.png", smallwidth=512, layers=[("edge", ("color", (0, 0, 1.0))), ("vertex", .007, ("color", (1.0, 0, 0)))] )
