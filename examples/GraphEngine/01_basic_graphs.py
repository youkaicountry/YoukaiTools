# 01_basic_graphs.py
# Basic examples of creating ans using graphs.


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


# First, import the GraphEngine module
import YoukaiTools.GraphEngine as GraphEngine

# Create an empty graph
graph = GraphEngine.BasicGraph()

# Add 3 vertices named "vertex_a", "vertex_b", and "vertex_c".
graph.addVertex("vertex_a")
graph.addVertex("vertex_b")
graph.addVertex("vertex_c")

# Connect "vertex_a" and "vertex_b" with an undirected edge named "edge_a",
# and "vertex_a" and "vertex_c" with an undirected edge named "edge_b".
graph.addEdge("vertex_a", "vertex_b", edgeid="edge_a")
graph.addEdge("vertex_a", "vertex_c", edgeid="edge_b")

# Print the list of vertices and edges.
print("Vertices: " + str(graph.getVertexList()))
print("Edges   : " + str(graph.getEdgeList()))

# Print the size and order of the graph
print("Order: " + str(graph.getOrder()))
print("Size : " + str(graph.getSize()))

# Print list of vertices adjacent to each vertex
for vertex in graph.getVertexList():
    print(vertex + " neighbors: " + str(graph.getAdjacentVertices(vertex)))
