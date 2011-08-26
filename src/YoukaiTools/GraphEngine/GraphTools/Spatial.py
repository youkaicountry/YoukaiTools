from YoukaiTools import ShiroiNeko
from . import Data
import random
import math

#have some kind of way to find the rotation that lines up the most edges
def rotate2D(g, rad):
    return

def calculateEdgeDistance2D(g, xpos="x", ypos="y", cost="cost", edgelist=None):
    if edgelist is None:
        edgelist = g.getEdgeList()
    for e in edgelist:
        v1, v2, d = g.getEdgeInfo(e)
        dx = g.getVertexData(v2, xpos) - g.getVertexData(v1, xpos)
        dy = g.getVertexData(v2, ypos) - g.getVertexData(v1, ypos)
        dist = math.sqrt(dx*dx + dy*dy)
        g.setEdgeInfo(e, cost, dist)
    return

#for the tuples, if t[0] is None, use t[1] as a value. If t[0] i snot none, use the value in that data field
def forceDraw2D(g, xpos="x", ypos="y", ke_cutoff=.001, ke_ncorrect=False, dt=.01, cycles_cutoff=None, vertexlist=None, edgelist=None, rand=None, initposition=True, mass=(None, 1), charge=(None, 1), spring=(None, 100), fluidfriction=.9, normalize=False, produce_history=False, history_cycles=10):
    if rand is None:
        rand = random.Random()
    if vertexlist is None:
        vertexlist = g.getVertexList()
    if edgelist is None:
        edgelist = g.getEdgeList()
    physics = ShiroiNeko.SN2D()
    physics.macrogravityon = False
    physics.coulombon = True
    physics.dt = dt
    physics.fluidfriction = fluidfriction
    for v in vertexlist:
        if initposition:
            g.setVertexData(v, xpos, rand.random())
            g.setVertexData(v, ypos, rand.random())
            physics.newParticle([v])
            physics.xposition[v] = g.getVertexData(v, xpos)
            
            physics.yposition[v] = g.getVertexData(v, ypos)
            physics.mass[v] = mass[1] if mass[0] is None else g.getVertexData(v, mass[0])
            physics.charge[v] = charge[1] if charge[0] is None else g.getVertexData(v, charge[0])
    for e in edgelist:
        ei = g.getEdgeInfo(e)
        physics.newBond(ei[0], ei[1], e, False)
        physics.spring[e] = spring[1] if spring[0] is None else g.getEdgeData(e, spring[0])
        physics.length[e] = 0
    uke_cutoff = ke_cutoff*g.getOrder() if ke_ncorrect else ke_cutoff
    cycle = 0
    history = {}
    while True:
        physics.update()
        cke = physics.getKineticEnergy()
        if produce_history:
            if (cycle % history_cycles) == 0:
                here = {}
                for v in g.getVertexList():
                    here[v] = {xpos:physics.xposition[v], ypos:physics.yposition[v]}
                history[cycle] = here
        print("KE: " + str(cke))
        if cke <= uke_cutoff: break
        cycle+=1
    for v in vertexlist:
        g.setVertexData(v, xpos, physics.xposition[v])
        g.setVertexData(v, ypos, physics.yposition[v])
    if normalize is not None:
        Data.normalizeDoubleVertexData(g, (xpos, ypos), vertexlist, normalize)
    return history
    