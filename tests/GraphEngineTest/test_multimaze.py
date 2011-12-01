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
