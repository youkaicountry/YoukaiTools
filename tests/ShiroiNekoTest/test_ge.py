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

r = random.Random()
#r = random.Random(1135)

def fitness(obj):
    sn2d = GR.graphToPhysics(obj)
    if not Game.clipBelow(sn2d):
        return 0
    if not Game.settleStructure2D(sn2d):
        return 0
    #return Game.scoreAverageHeight(sn2d)
    #return Game.scoreHeight(sn2d)
    return Game.scoreWeightHeight(sn2d)

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
            ab = GR.randomAddBond(graph, 2, r)
            if ab is not None:
                GR.addBondToGraph(graph, ab[0], ab[1], 1200, 8000)
        elif ri == 1:
            GR.randomDelBond(graph, r)
        elif ri == 2:
            ab = GR.randomAddParticle(graph, 1.0, 2.0, r)
            if ab is not None:
                np = GR.addParticleToGraph(graph, ab[1], ab[2], 0, 0, 0, 0, 1, False, 0)
                GR.addBondToGraph(graph, ab[0], np, 1200, 8000)
        elif ri == 3:
            ab = GR.randomJostleParticle(graph, 0.0, .2, .5, 3.0)
    return graph

def random_dna():
    graph = GraphEngine.BasicGraph()
    GR.addGlobalToGraph(graph, .02, True, 9.81, 0.0, False, .98, False, 0)
    p1 = GR.addParticleToGraph(graph, 0, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p1 = GR.addParticleToGraph(graph, .5, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p2 = GR.addParticleToGraph(graph, 1, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p1 = GR.addParticleToGraph(graph, 1.5, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p3 = GR.addParticleToGraph(graph, 2, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p1 = GR.addParticleToGraph(graph, 2.5, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p4 = GR.addParticleToGraph(graph, 3, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p1 = GR.addParticleToGraph(graph, 3.5, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    return graph
    
def basic_dna():
    graph = GraphEngine.BasicGraph()
    GR.addGlobalToGraph(graph, .02, True, 9.81, 0.0, False, .98, False, 0)
    p1 = GR.addParticleToGraph(graph, 0, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p1 = GR.addParticleToGraph(graph, .5, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p2 = GR.addParticleToGraph(graph, 1, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p1 = GR.addParticleToGraph(graph, 1.5, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p3 = GR.addParticleToGraph(graph, 2, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p1 = GR.addParticleToGraph(graph, 2.5, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p4 = GR.addParticleToGraph(graph, 3, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    p1 = GR.addParticleToGraph(graph, 3.5, 0, 0, 0, 0, 0, 1, True, 0, important=True)
    return graph

def report(report):
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

reportc = GeneAlg.make_criteria(None, 50)
savec = GeneAlg.make_criteria(None, 1000)
termc = GeneAlg.make_criteria(1, None)

GA.run(reportc, savec, termc)
ab = GA.getBest()
Draw.drawSimple(ab[1], "tower_img.png", ("xposition", "yposition"))

#make a graph image
dg = PyRange.DataGraph1D(default_interp=PyRange.Interpolation.linear)


dg.setFromXY(fitnessx, fitnessy)
Draw1D.saveDataGraph1DFile("./tower_score.png", dg)
