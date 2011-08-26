from YoukaiTools import GraphEngine
from YoukaiTools.GraphEngine.GraphTools.SpecialTypes import GridGraph
from YoukaiTools.MazeGen.generators import maze as maze

rbt = maze.recursiveBacktrackMaze()
rbt.make(7, 7, blocked=False)
bm = rbt.get("blockmap")

bg = GraphEngine.Graphs.BasicGraph()
GridGraph.buildGridGraphFromBlockMap(bg, bm)

rg = GraphEngine.BasicGraph()
GraphEngine.GraphTools.SubGraph.corridorGraphReduction(bg, rg, reversepathname="reversepath")

print("before force")
GraphEngine.GraphTools.Spatial.forceDraw2D(bg, normalize=(0, 1), ke_cutoff=.5)
GraphEngine.GraphTools.Spatial.forceDraw2D(rg, normalize=(0, 1), ke_cutoff=.5)
print("after force")

GraphEngine.Draw.drawSimple(bg, "./output/maze_full_force.bmp", smallwidth=512, layers=[("edge", ("color", (0, 0, 1.0))), ("vertex", .007, ("color", (1.0, 0, 0)))] )
GraphEngine.Draw.drawSimple(rg, "./output/maze_reduced_force.bmp", smallwidth=512, layers=[("edge", ("color", (0, 0, 1.0))), ("vertex", .007, ("color", (1.0, 0, 0)))] )
