import random
import YoukaiTools.Circuit as Circuit
import YoukaiTools.ImageTools as ImageTools
import YoukaiTools.AdvRandom as AdvRandom
from YoukaiTools import GeneAlg
import YoukaiTools.PyRange as PyRange
import YoukaiTools.PyRange.Draw.Draw1D as Draw1D
import math

fitnessx = []
fitnessy = []

mf = Circuit.Chips.NeuralNet.thresh_meanfield
nn = Circuit.Chips.NeuralNet.ForwardFeedNeuralNetwork([3, 8, 8, 3], [1.0, 1.0, 1.0, 1.0], [mf, mf, mf, mf])
#nn = Circuit.Chips.NeuralNet.ForwardFeedNeuralNetwork([3, 5, 3], [1.0, 1.0, 1.0], [mf, mf, mf])
ss = set(["in0", "in1", "in2"])
vs = set([x for x in nn.inputs.keys()])
vars = {}
for v in vs-ss:
    vars[v] = (v, 0)    
vc = Circuit.Chips.Cases.VariableChip(nn, vars)
print(vc.getVariableList())

test_cases = []
for i in range(110):
    rgb = (random.random(), random.random(), random.random())
    hsi = ImageTools.ColorModels.RGB2HSI(rgb)
    test_cases.append((rgb, hsi))

def fitness(obj):
    mindiff = .000001
    sum = 0
    for t in test_cases:
        for k in obj.keys():
            vc.setVariable(k, obj[k])
        for i, x in enumerate(t[0]):
            vc.setInput("in"+str(i), x)
        vc.doCalculation()
        for i, x in enumerate(t[1]):
            if i == 0:
                v = vc.getOutput("out"+str(i))
                if v < 0.0 or v > 1.0:
                    diff = 1.0
                else:
                    mi = min(x, v)
                    ma = max(x, v)
                    diff = min(abs(v - x), (1.0-ma)+mi)
                    diff = max(diff, mindiff)
                sum += (1.0/diff)*2.0
            else:
                diff = abs(vc.getOutput("out"+str(i)) - x)
                diff = max(diff, mindiff)
                m = 1.0 if i == 1 else .5
                sum += (1.0/diff)*m
    return math.log(sum)

def mate(obj1, obj2):
    d = {}
    r = random.randint(0, 1)
    if r == 0:
        d.update(obj1)
    else:
        d.update(obj2)
    return d

def mutate(intensity, obj):
    ol = [k for k in obj.keys()]
    random.shuffle(ol)
    d = {}
    nums = []
    chan = []
    for i in range(len(ol)/3):
        nums.append(i+1)
        chan.append(1.0/(float(i)+1.0))
    n = AdvRandom.biasedChoice(nums, chan)
    for k in ol[:n]:
        v = (random.random()*intensity*2.0)-intensity
        d[k] = obj[k] + v
    for k in ol[n:]:
        d[k] = obj[k]
    return d

def random_dna():
    o = {}
    for k in vc.getVariableList():
        o[k] = random.random()
    return o
    
def basic_dna():
    o = {}
    for k in vc.getVariableList():
        o[k] = 0
    return o

def report(obj,fitness,generation,topgeneration):
    print("GENERATION: " + str(generation))
    print("PROGRESS: " + str(round(float(generation)/float(topgeneration), 6)*100.0)+"%")
    print("TOP: " + str(fitness))
    fitnessx.append(generation)
    fitnessy.append(fitness)
    print("")
    return

st = GeneAlg.SelectionTypes.tourney_select
dt = GeneAlg.SelectionTypes.tourney_low_select
fill = GeneAlg.FillTypes.random_fill
gene = GeneAlg.make_gene(fitness, mate, mutate, random_dna, basic_dna, report = report)

#op = GeneAlg.make_options(st, (10,), dt, (10,), fill, (), 1.0, .00, .75)
#GA = GeneAlg.Algorithms.Pool(gene, op, 300)

op = GeneAlg.make_options(st, (1,), dt, (1,), fill, (), 1.0, .00, 1.0)
GA = GeneAlg.Algorithms.HillClimb(gene, op)

#op = GeneAlg.make_options(st, (2,), dt, (2,), fill, (), 1.0, .00, .75)
#GA = GeneAlg.Algorithms.Community(gene, op, 15)

GA.doGeneration(500000, 100)
ab = GA.getBest()
print ab
#test our function!
for i in range(3):
    rgb = (random.random(), random.random(), random.random())
    hsi = ImageTools.ColorModels.RGB2HSI(rgb)
    for k in ab[1].keys():
        vc.setVariable(k, ab[1][k])
    for i in range(3):
        vc.setInput("in"+str(i), rgb[i])
    vc.doCalculation()
    nnhsi = (vc.getOutput("out0"), vc.getOutput("out1"), vc.getOutput("out2"))
    print("RGB:    " + str(rgb))
    print("HSI:    " + str(hsi))
    print("NN HSI: " + str(nnhsi))

#make a graph image
dg = PyRange.DataGraph1D(default_interp=PyRange.Interpolation.linear)
dg.setFromXY(fitnessx, fitnessy)
Draw1D.saveDataGraph1DFile("./hill6.png", dg)
