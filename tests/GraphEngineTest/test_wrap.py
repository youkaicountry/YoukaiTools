# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# Import the GraphEngine module
import YoukaiTools.GraphEngine as GraphEngine

# Create an empty graph
graph = GraphEngine.BasicGraph()

# Make a grid, like might appear in an overhead game
# To do this, we will use the BlockMap class from
# MazeGen.
# First, import it
import YoukaiTools.MazeGen.datatypes

# Make a small 5x5 world for this example
bmap = YoukaiTools.MazeGen.datatypes.BlockMap(3, 3)

# Put some walls in it by setting them to True
bmap.setSpaces([(0, 0), (0, 1), (1, 0)], True)

# Now make a graph out of it
# First we import the 'special types' GridGraph
import YoukaiTools.GraphEngine.GraphTools.SpecialTypes.GridGraph as GridGraph

# Now call the buildGridGraphFromBlockMap function
GridGraph.buildGridGraphFromBlockMap(graph, bmap)

GridGraph.enforceWrap(graph, (0, 2), (0, 2), True, True)

print(GraphEngine.GraphTools.Notation.toEdgeMathNotation(graph))
