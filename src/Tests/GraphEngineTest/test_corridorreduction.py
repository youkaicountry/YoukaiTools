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
