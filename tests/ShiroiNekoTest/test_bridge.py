import random
import math

import YoukaiTools.Circuit as Circuit
import YoukaiTools.ImageTools as ImageTools
import YoukaiTools.AdvRandom as AdvRandom
from YoukaiTools import GeneAlg
import YoukaiTools.PyRange as PyRange
import YoukaiTools.PyRange.Draw.Draw1D as Draw1D
import YoukaiTools.GraphEngine as GraphEngine
from YoukaiTools.GraphEngine import Draw
import YoukaiTools.ShiroiNeko.GraphRepresentation as GR
import YoukaiTools.ShiroiNeko.Game as Game
import YoukaiTools.GraphEngine.GraphTools.SubGraph as SubGraph

fitnessx = []
fitnessy = []

bspring = 2000
bforce = 3200
udt = .013

mindist = .5
maxdist = 1.99

r = random.Random()
#r = random.Random(1135)

def fitness(obj):
    #for p in obj.getVertexList():
    #    if 'xposition' in obj.getVertexDataKeys(p):
    #        print(str(p) + ": " + str(obj.getVertexData(p, 'xposition')) + ", " + str(obj.getVertexData(p, 'yposition')))
    #if obj.getOrder() == 9:
    #    print("HONK")
    #    return 0
    #print(['important' in obj.getVertexDataKeys(v) for v in obj.getVertexList()])
    if all(['important' in obj.getVertexDataKeys(v) for v in obj.getVertexList() if v != 'global']):
        return 0
    sn2d = GR.graphToPhysics(obj)
    if not Game.clipBelow(sn2d, 5):
        return 0
    if not Game.settleStructure2D(sn2d):
        return 0
    #return Game.scoreAverageHeight(sn2d)
    #return Game.scoreHeight(sn2d)
    vertices = [v for v in obj.getVertexList() if ((v != 'global') and (not obj.getVertexData(v, 'fixed')))]
    return Game.scoreWeight(sn2d, vertices=vertices)

def mate(obj1, obj2):
    a = [obj1, obj2]
    return a[r.randint(0, 1)]

def mutate(intensity, obj):
    minimum = 1
    maximum = 5 if obj.getOrder() < 10 else int(obj.getOrder()/2)+3
    ui = int((intensity*(maximum-minimum))+minimum)
    #ui = int(max(4, intensity*(obj.getOrder()/2)))
    graph = GraphEngine.BasicGraph()
    SubGraph.copyGraph(graph, obj)
    for i in xrange(ui):
        ri = r.randint(0,3)
        if ri == 0:
            ab = GR.randomAddBond(graph, maxdist, r)
            if ab is not None:
                GR.addBondToGraph(graph, ab[0], ab[1], bspring, bforce)
        elif ri == 1:
            GR.randomDelBond(graph, r)
        elif ri == 2:
            ab = GR.randomAddParticle(graph, mindist, maxdist, r)
            if ab is not None:
                np = GR.addParticleToGraph(graph, ab[1], ab[2], 0, 0, 0, 0, 1, False, 0)
                GR.addBondToGraph(graph, ab[0], np, bspring, bforce)
        elif ri == 3:
            ab = GR.randomJostleParticle(graph, 0.0, .5, mindist, maxdist)
    return graph

def random_dna():
    graph = GraphEngine.BasicGraph()
    GR.addGlobalToGraph(graph, udt, True, 9.81, 0.0, False, .98, False, 0)
    pbase1 = GR.addParticleToGraph(graph, -1, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    pbase2 = GR.addParticleToGraph(graph, 8, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    pbase3 = GR.addParticleToGraph(graph, -1, -1, 0, 0, 0, 0, 1, True, 0, important=True)
    pbase4 = GR.addParticleToGraph(graph, 8, -1, 0, 0, 0, 0, 1, True, 0, important=True)
    pbase1 = GR.addParticleToGraph(graph, 0, 1, 0, 0, 0, 0, 1, True, 0, important=True)
    pbase1 = GR.addParticleToGraph(graph, 0, 2, 0, 0, 0, 0, 1, True, 0, important=True)
    pbase1 = GR.addParticleToGraph(graph, 8, 1, 0, 0, 0, 0, 1, True, 0, important=True)
    pbase1 = GR.addParticleToGraph(graph, 8, 2, 0, 0, 0, 0, 1, True, 0, important=True)
    
    p1 = GR.addParticleToGraph(graph, 0, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p2 = GR.addParticleToGraph(graph, 1, 0, 0, 0, 0, 0, 1, False, 0, important=True)
    GR.addBondToGraph(graph, p1, p2, bspring, bforce, important=True)
    
    p3 = GR.addParticleToGraph(graph, 2, 0, 0, 0, 0, 0, 1, False, 0, important=True)
    GR.addBondToGraph(graph, p2, p3, bspring, bforce, important=True)
    
    p4 = GR.addParticleToGraph(graph, 3, 0, 0, 0, 0, 0, 1, False, 0, important=True)
    GR.addBondToGraph(graph, p3, p4, bspring, bforce, important=True)
    
    p5 = GR.addParticleToGraph(graph, 4, 0, 0, 0, 0, 0, 1, False, 0, important=True)
    GR.addBondToGraph(graph, p4, p5, bspring, bforce, important=True)
    
    p6 = GR.addParticleToGraph(graph, 5, 0, 0, 0, 0, 0, 1, False, 0, important=True)
    GR.addBondToGraph(graph, p5, p6, bspring, bforce, important=True)
    
    p7 = GR.addParticleToGraph(graph, 6, 0, 0, 0, 0, 0, 1, False, 0, important=True)
    GR.addBondToGraph(graph, p6, p7, bspring, bforce, important=True)
    
    p8 = GR.addParticleToGraph(graph, 7, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    GR.addBondToGraph(graph, p7, p8, bspring, bforce, important=True)
    return graph
    
def basic_dna():
    graph = GraphEngine.BasicGraph()
    GR.addGlobalToGraph(graph, udt, True, 9.81, 0.0, False, .98, False, 0)
    p1 = GR.addParticleToGraph(graph, 0, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p2 = GR.addParticleToGraph(graph, 1, 0, 0, 0, 0, 0, 1, False, 0, important=True)
    GR.addBondToGraph(graph, p1, p2, bspring, bforce, important=True)
    
    p3 = GR.addParticleToGraph(graph, 2, 0, 0, 0, 0, 0, 1, False, 0, important=True)
    GR.addBondToGraph(graph, p2, p3, bspring, bforce, important=True)
    
    p4 = GR.addParticleToGraph(graph, 3, 0, 0, 0, 0, 0, 1, False, 0, important=True)
    GR.addBondToGraph(graph, p3, p4, bspring, bforce, important=True)
    
    p5 = GR.addParticleToGraph(graph, 4, 0, 0, 0, 0, 0, 1, False, 0, important=True)
    GR.addBondToGraph(graph, p4, p5, bspring, bforce, important=True)
    
    p6 = GR.addParticleToGraph(graph, 5, 0, 0, 0, 0, 0, 1, False, 0, important=True)
    GR.addBondToGraph(graph, p5, p6, bspring, bforce, important=True)
    
    p7 = GR.addParticleToGraph(graph, 6, 0, 0, 0, 0, 0, 1, False, 0, important=True)
    GR.addBondToGraph(graph, p6, p7, bspring, bforce, important=True)
    
    p8 = GR.addParticleToGraph(graph, 7, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    GR.addBondToGraph(graph, p7, p8, bspring, bforce, important=True)
    return graph

def report(report):
    o = report['top_object']
    print("GENERATION: " + str(report["generation"]))
    #print("PROGRESS: " + str(round(float(report["generation"])/float(report["termination_generation"]), 6)*100.0)+"%")
    print("TIME: " + str(report["time"]))
    print("generation: "+str(report["generation"]))
    print("TOP: " + str(report["top_fitness"]))
    fitnessx.append(report["generation"])
    fitnessy.append(report["top_fitness"])
    print("")
    return

st = GeneAlg.SelectionTypes.tourney_select
dt = GeneAlg.SelectionTypes.tourney_low_select
fill = GeneAlg.FillTypes.random_fill
gene = GeneAlg.make_gene(fitness, mate, mutate, random_dna, basic_dna, report = report)

op = GeneAlg.make_options(st, (6,), dt, (6,), fill, (), 1.0, .00, 1.0)
GA = GeneAlg.Algorithms.Pool(gene, op, 400)

#op = GeneAlg.make_options(st, (1,), dt, (1,), fill, (), 1.0, .00, 1.0)
#GA = GeneAlg.Algorithms.HillClimb(gene, op)

#op = GeneAlg.make_options(st, (1,), dt, (1,), fill, (), 1.0, .00, 1.0)
#GA = GeneAlg.Algorithms.MultiHillClimb(gene, op)

#op = GeneAlg.make_options(st, (2,), dt, (2,), fill, (), 1.0, .00, .75)
#GA = GeneAlg.Algorithms.Community(gene, op, 15)

reportc = GeneAlg.make_criteria(None, 20)
savec = GeneAlg.make_criteria(None, 1000)
termc = GeneAlg.make_criteria(60*60, None)

GA.run(reportc, savec, termc)
ab = GA.getBest()
Draw.drawSimple(ab[1], "bridge_img.png", ("xposition", "yposition"))

#make a graph image
dg = PyRange.DataGraph1D(default_interp=PyRange.Interpolation.linear)

print(ab[1].getSize())

dg.setFromXY(fitnessx, fitnessy)
Draw1D.saveDataGraph1DFile("./bridge_score.png", dg)
