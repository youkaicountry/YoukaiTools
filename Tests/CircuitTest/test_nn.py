import random
import YoukaiTools.Circuit as Circuit
import YoukaiTools.ImageTools as ImageTools
import YoukaiTools.AdvRandom as AdvRandom
from YoukaiTools import GeneAlg

mf = Circuit.Chips.NeuralNet.thresh_meanfield
nn = Circuit.Chips.NeuralNet.ForwardFeedNeuralNetwork([3, 4, 4, 3], [1.0, 1.0, 1.0, 1.0], [mf, mf, mf, mf])
ss = set(["in0", "in1", "in2"])
vs = set([x for x in nn.inputs.keys()])
vars = {}
for v in vs-ss:
    vars[v] = (v, 0)    
vc = Circuit.Chips.Cases.VariableChip(nn, vars)

test_cases = []
for i in range(100):
    rgb = (random.random(), random.random(), random.random())
    hsi = ImageTools.ColorModels.RGB2HSI(rgb)
    test_cases.append((rgb, hsi))

def fitness(obj):
    mindiff = .00000000001
    sum = 0
    for t in test_cases:
        for k in obj.keys():
            vc.setVariable(k, obj[k])
        for i, x in enumerate(t[0]):
            vc.setInput("in"+str(i), x)
        vc.doCalculation()
        for i, x in enumerate(t[1]):
            diff = abs(vc.getOutput("out"+str(i)) - x)
            diff = max(diff, mindiff)
            sum += 1.0/diff
    return sum

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

st = GeneAlg.SelectionTypes.tourney_select
dt = GeneAlg.SelectionTypes.tourney_low_select
fill = GeneAlg.FillTypes.random_fill
op = GeneAlg.make_options(st, (5,), dt, (5,), fill, (), 1.0, .00, 1.0)
gene = GeneAlg.make_gene(fitness, mate, mutate, random_dna, basic_dna)
GA = GeneAlg.Algorithms.Pool(gene, op, 200)
GA.doGeneration(1000, 100)
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