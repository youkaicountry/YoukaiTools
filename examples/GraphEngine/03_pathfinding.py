# 02_graph_building.py
# Easily creating larger graphs using graph builders.


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
import YoukaiTools.MapData.datatypes

# Make a small 5x5 world for this example
bmap = YoukaiTools.MapData.datatypes.BlockMap(5, 5)

# Put some walls in it by setting them to True
bmap.setSpaces([(2, 0), (2, 1), (2, 2), (2, 4)], True)

# Now make a graph out of it
# First we import the 'special types' GridGraph
import YoukaiTools.GraphEngine.GraphTools.SpecialTypes.GridGraph as GridGraph

# Now call the buildGridGraphFromBlockMap function
GridGraph.buildGridGraphFromBlockMap(graph, bmap)

# graph now contains a graph representing our map.
# Let's do standard game style A* pathfinding on the map
# from space (0, 0) to space (4, 0).
# Of course A* needs a heuristic. The default it tries to use
# is euclidean2d. It looks at the data values 'x' and 'y' of your
# nodes. Those have already been set automatically by the
# buildGridGraphFromBlockmap function, but if you are rolling
# your own graph, then you will need to set them.

# Import the pathfinding module
import YoukaiTools.GraphEngine.GraphTools.Paths as Paths

# Now run the algorithm
path = Paths.AStarPath(graph, (0, 0), (4, 0))

# What it returns is a list of tuples that make up the path.
# The tuples each contain a vertex, and the next edge in the path.
# so the output looks like this [(vertex, edge), (vertex, edge), ...]
print(path)
