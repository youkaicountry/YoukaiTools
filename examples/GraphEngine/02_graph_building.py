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
#import YoukaiTools.GraphEngine.Builders as Builders

# Create an empty graph
graph = GraphEngine.BasicGraph()

# Add 20 vertices to the graph
GraphEngine.GraphTools.Builders.buildGraph(graph, 20)

# Print the vertices in the graph
print("Vertices: " + str(graph.getVertexList()))

# Make a new graph
graph2 = GraphEngine.BasicGraph()

# Make a list of vertices and edges we wish the graph to have
vertices = ["va", "vb", "vc", "vd", "ve", "vf", "vg"]
edges = [("va", "vb"), ("vb", "vc"), ("vb", "vd"), ("vf", "vg")]

# Build a graph using those vertices and edges
GraphEngine.GraphTools.Builders.buildGraph(graph2, vertices, edges)

# Print the vertices and edges
print("Vertices: " + str(graph2.getVertexList()))
print("Edges   : " + str(graph2.getEdgeList()))

# Make a third graph
graph3 = GraphEngine.BasicGraph()

# Make a vertex dictionary, and add data to the vertices
vdic = {}
vdic["va"] = {"name":"va", "data":{"cost":1}}
vdic["vb"] = {"name":"vb", "data":{"cost":3}}
vdic["vc"] = {"name":"vc", "data":{"cost":2.1}}

# Make an edge dictionary, and add data to the edges as well
edic = {}
edic["ea"] = {"name":"ea", "vertices":("va","vb"), "data":{"cost":4}}
edic["eb"] = {"name":"eb", "vertices":("va","vc"), "data":{"cost":4.2}}

# Build the graph using the dictionaries
GraphEngine.GraphTools.Builders.buildGraphD(graph3, vdic, edic)

# Print the vertices, edges, and their data
for v in graph3.getVertexList():
    print(v)
    print("data:")
    for k in graph3.getVertexDataKeys(v):
        print("   " + str(k) + ": " + str(graph3.getVertexData(v, k)))

for e in graph3.getEdgeList():
    print(e)
    print("data:")
    for k in graph3.getEdgeDataKeys(e):
        print("   " + str(k) + ": " + str(graph3.getEdgeData(e, k)))
