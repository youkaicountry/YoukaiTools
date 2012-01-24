import random

import YoukaiTools.GraphEngine as GraphEngine
from YoukaiTools.GraphEngine import Draw
import YoukaiTools.ShiroiNeko.GraphRepresentation as GR
import YoukaiTools.ShiroiNeko.Game as Game


r = random.Random()

i = 0
while True:
    print(i)
    graph = GraphEngine.BasicGraph()
    GR.addGlobalToGraph(graph, .02, True, 9.81, 0.0, False, .98, False, 0)
    p1 = GR.addParticleToGraph(graph, 0, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p2 = GR.addParticleToGraph(graph, 1, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p3 = GR.addParticleToGraph(graph, .5, .5, 0, 0, 0, 0, 1, True, 0, important=True)
    for i in range(20):
        ri = r.randint(0,2)
        if ri == 0:
            ab = GR.randomAddBond(graph, 1, r)
            if ab is not None:
                GR.addBondToGraph(graph, ab[0], ab[1], 1000, 100)
        elif ri == 1:
            GR.randomDelBond(graph, r)
        elif ri == 2:
            ab = GR.randomAddParticle(graph, .5, 1, r)
            if ab is not None:
                np = GR.addParticleToGraph(graph, ab[1], ab[2], 0, 0, 0, 0, 1, False, 0)
                GR.addBondToGraph(graph, ab[0], np, 1000, 100)
    if Game.settleStructure2D(GR.graphToPhysics(graph)): break
    i += 1
Draw.drawSimple(graph, "random.png", ("xposition", "yposition"))

#sn2d = GR.graphToPhysics(graph)

#for i in xrange(200):
#    sn2d.update()
#    if i % 20 == 0:
#        g2 = GraphEngine.BasicGraph()
#        GR.physicsToGraph(sn2d, g2)
#        Draw.drawSimple(g2, str(i)+".png", ("xposition", "yposition"))
