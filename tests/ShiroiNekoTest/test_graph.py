import YoukaiTools.GraphEngine as GraphEngine
from YoukaiTools.GraphEngine import Draw
import YoukaiTools.ShiroiNeko.GraphRepresentation as GR

graph = GraphEngine.BasicGraph()
GR.addGlobalToGraph(graph, .02, True, 9.81, 0.0, False, .98, False, 0)
p1 = GR.addParticleToGraph(graph, 0, 0, 0, 0, 0, 0, 1, True, 0)
p2 = GR.addParticleToGraph(graph, 2, 0, 0, 0, 0, 0, 1, False, 0)
p3 = GR.addParticleToGraph(graph, 1, -2, 0, 0, 0, 0, 1, True, 0)
GR.addBondToGraph(graph, p1, p2, 1000, 100)

sn2d = GR.graphToPhysics(graph)

for i in xrange(200):
    sn2d.update()
    if i % 20 == 0:
        g2 = GraphEngine.BasicGraph()
        GR.physicsToGraph(sn2d, g2)
        Draw.drawSimple(g2, str(i)+".png", ("xposition", "yposition"))