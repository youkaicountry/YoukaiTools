from YoukaiTools import GraphEngine
import random
from YoukaiTools.GraphEngine.GraphTools.SpecialTypes import GridGraph
from YoukaiTools.GraphEngine.GraphTools.Span import Worms

kruskal_animation = False
recurse_animation = False
prim_animation = False

size = (24, 24)

#make the basic setup
bg = GraphEngine.Graphs.BasicGraph()
GridGraph.buildGridGraph(bg, dimensions=size)

#make the random instance
r = random.Random()

#kruskal
kedges = GraphEngine.GraphTools.Span.kruskal(bg, r=r)
kg = GraphEngine.Graphs.BasicGraph()
GraphEngine.GraphTools.SubGraph.copyGraph(kg, bg, edgelist=kedges)
#pathfind it
paths = GraphEngine.GraphTools.Paths.dijkstraPaths(kg, (0, 0), [(size[0]-1, size[1]-1)])
for path in paths:
    GraphEngine.GraphTools.Data.setDataToPath(kg, path, vertexdata=("color", (0, 1, 0)), edgedata=("color", (0, 1, 0)))

#recursiveBacktrack
redges = GraphEngine.GraphTools.Span.recursiveBacktrack(bg, r=r, start=(0, 0))
rg = GraphEngine.Graphs.BasicGraph()
GraphEngine.GraphTools.SubGraph.copyGraph(rg, bg, edgelist=redges)
#pathfind it
paths = GraphEngine.GraphTools.Paths.dijkstraPaths(rg, (0, 0), [(size[0]-1, size[1]-1)])
for path in paths:
    GraphEngine.GraphTools.Data.setDataToPath(rg, path, vertexdata=("color", (0, 1, 0)), edgedata=("color", (0, 1, 0)))

#prim
pedges = GraphEngine.GraphTools.Span.prim(bg, r=r, start=(0, 0))
pg = GraphEngine.Graphs.BasicGraph()
GraphEngine.GraphTools.SubGraph.copyGraph(pg, bg, edgelist=pedges)
#pathfind it
paths = GraphEngine.GraphTools.Paths.dijkstraPaths(pg, (0, 0), [(size[0]-1, size[1]-1)])
for path in paths:
    GraphEngine.GraphTools.Data.setDataToPath(pg, path, vertexdata=("color", (0, 1, 0)), edgedata=("color", (0, 1, 0)))

#worms
#cow = Worms.CanOfWorms(bg)
#wedges = cow.go(10)
#wg = GraphEngine.Graphs.BasicGraph()
#GraphEngine.GraphTools.SubGraph.copyGraph(wg, bg, edgelist=wedges)
#pathfind it
#paths = GraphEngine.GraphTools.Paths.dijkstraPaths(pg, (0, 0), [(size[0]-1, size[1]-1)])
#for path in paths:
#    GraphEngine.GraphTools.Data.setDataToPath(pg, path, vertexdata=("color", (0, 1, 0)), edgedata=("color", (0, 1, 0)))

#produce kruskal animation
if kruskal_animation:
    ag = GraphEngine.Graphs.BasicGraph()
    for i in range(len(kedges)):
        print("Rendering Kruskal " + str(i+1) + "/" + str(len(kedges)))
        ag.clearGraph()
        GraphEngine.GraphTools.SubGraph.copyGraph(ag, bg, edgelist=kedges[:i+1])
        GraphEngine.Draw.drawSimple(ag, "./output/animation/kruskal_build/build_" + str(i) + ".png", smallwidth=512, layers=[("vertex", .003, ("color", (.15, .15, .15))), ("edge", ("color", (0, 0, 1.0)))] )

#produce recurse animation
if recurse_animation:
    ag = GraphEngine.Graphs.BasicGraph()
    for i in range(len(redges)):
        print("Rendering Recurse " + str(i+1) + "/" + str(len(redges)))
        ag.clearGraph()
        GraphEngine.GraphTools.SubGraph.copyGraph(ag, bg, edgelist=redges[:i+1])
        GraphEngine.Draw.drawSimple(ag, "./output/animation/recurse_build/build_" + str(i) + ".png", smallwidth=512, layers=[("vertex", .003, ("color", (.15, .15, .15))), ("edge", ("color", (0, 0, 1.0)))] ) 
        
#produce prim animation
if prim_animation:
    ag = GraphEngine.Graphs.BasicGraph()
    for i in range(len(pedges)):
        print("Rendering Prim " + str(i+1) + "/" + str(len(redges)))
        ag.clearGraph()
        GraphEngine.GraphTools.SubGraph.copyGraph(ag, bg, edgelist=pedges[:i+1])
        GraphEngine.Draw.drawSimple(ag, "./output/animation/prim_build/build_" + str(i) + ".png", smallwidth=512, layers=[("vertex", .003, ("color", (.15, .15, .15))), ("edge", ("color", (0, 0, 1.0)))] )    

GraphEngine.Draw.drawSimple(kg, "./output/maze_kruskal.png", smallwidth=512, layers=[("vertex", .007, ("color", (1.0, 0, 0))), ("edge", ("color", (0, 0, 1.0)))] )
GraphEngine.Draw.drawSimple(rg, "./output/maze_recurse.png", smallwidth=512, layers=[("vertex", .007, ("color", (1.0, 0, 0))), ("edge", ("color", (0, 0, 1.0)))] )
GraphEngine.Draw.drawSimple(pg, "./output/maze_prim.png", smallwidth=512, layers=[("vertex", .007, ("color", (1.0, 0, 0))), ("edge", ("color", (0, 0, 1.0)))] )
#GraphEngine.Draw.drawSimple(wg, "./output/maze_worms.png", smallwidth=512, layers=[("vertex", .007, ("color", (1.0, 0, 0))), ("edge", ("color", (0, 0, 1.0)))] )
