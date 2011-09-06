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
