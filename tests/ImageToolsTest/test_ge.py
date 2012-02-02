import random
import math
import cPickle
import gzip
import sys

import YoukaiTools.ImageTools as ImageTools
from YoukaiTools.ImageTools.FileHandlers import PNG
from YoukaiTools import GeneAlg
import YoukaiTools.PyRange as PyRange
import YoukaiTools.PyRange.Draw.Draw1D as Draw1D
import YoukaiTools.GraphEngine as GraphEngine
from YoukaiTools.GraphEngine import Draw
import YoukaiTools.GraphEngine.GraphTools.SubGraph as SubGraph

fitnessx = []
fitnessy = []

r = random.Random()
#r = random.Random(1135)

mixmethod2func = {}
mixmethod2func['add'] = ImageTools.CombineFunctions.add
mixmethod2func['subtract'] = ImageTools.CombineFunctions.sub
mixmethod2func['average'] = ImageTools.CombineFunctions.average
mixmethod2func['multiply'] = ImageTools.CombineFunctions.multiply
mixmethod2func['paint'] = ImageTools.CombineFunctions.paint

drawmode2num = {}
drawmode2num["line"] = 2
drawmode2num["triangle"] = 3

#--------- IO
#The target image to attempt to draw
target_image = PNG.loadFile(sys.argv[1])[0]
#The output image
output_image = sys.argv[2]
#The input pickle filename
output_pickle = sys.argv[3] if len(sys.argv) > 3 else None
#The output pickle filename
input_pickle = sys.argv[4] if len(sys.argv) > 4 else None

# -------- OPTIONS
#The number of elements to use in creating the image
tris = 50
#Whether to resize laoded arrays or not
resize_arrays = True
#The maximum mutation intensity
max_mutation_intensity = .2
#Can the elements warp, or only move?
warp = True
#Chance of a warp
warp_chance = .2
#The maximum number of mutations to attempt each cycle
max_mutates = 3
#The mix method to use for painting
mix_method = "subtract"
#Number of hours to run the simulation
hours_to_run = .5
#Report every how many generations?
report_every = 50
#draw after an improvement of:
history_after = 1.001

draw_mode = "triangle" #line or triangle

start_element_color_min = [0.0, 1.0, 1.0]
start_element_color_max = [0.0, 1.0, 1.0]
start_background_color = [1.0, 1.0, 1.0]
start_element_range = ((0.0, 1.0), (0.0, 1.0))
#start_element_offset = ((-1.0, 1.0), (-1.0, 1.0))
start_element_offset = ((-.2, .2), (-.2, .2))

element_color_locked = True
# --------

max_fitness = float(target_image[0]*target_image[1]*target_image[2])

last_drawn = 0

if len(start_element_color_min) > target_image[2]:
    start_element_color_min = start_element_color_min[:target_image[2]]
    start_element_color_max = start_element_color_max[:target_image[2]]
elif len(start_element_color_min) < target_image[2]:
    while len(start_element_color_min) < target_image[2]:
        start_element_color_min.append(0.0)
        start_element_color_max.append(0.0)

if len(start_background_color) > target_image[2]:
    start_background_color = start_background_color[:target_image[2]]
elif len(start_background_color) < target_image[2]:
    while len(start_background_color) < target_image[2]:
        start_background_color.append(0.0)

use_gene = None
if input_pickle is not None:
    f = gzip.open(input_pickle, "r")
    use_gene = cPickle.load(f)
    f.close()
    
def makeImage(obj):
    w = target_image[0]
    h = target_image[1]
    mm = mixmethod2func[mix_method]
    img = ImageTools.Create.newImage(w, h, start_background_color)
    #w -=1
    #h-=1
    if draw_mode == "triangle":
        for tri in obj:
            ImageTools.Modify.drawFilledTriangle(img, int(tri[0]*w), int(tri[1]*h), int(tri[2]*w), int(tri[3]*h), int(tri[4]*w), int(tri[5]*h),  tri[6:], mm)
    elif draw_mode == "line":
        w-=1
        h-=1
        for tri in obj:
            ImageTools.Modify.drawLine(img, int(tri[0]*w), int(tri[1]*h), int(tri[2]*w), int(tri[3]*h), tri[4:], mm)
    return img

def fitness(obj):
    img = makeImage(obj)
    f = ImageTools.Comparison.manhattanDistance(img, target_image)
    return max_fitness - f

def mate(obj1, obj2):
    a = [obj1, obj2]
    return a[r.randint(0, 1)]

def mutate(intensity, obj):
    out = [x[:] for x in obj]
    to_mutate = min(max((int(len(obj)*intensity), 1)), max_mutates)
    #if to_mutate < 1: to_mutate = 1
    for n in xrange(to_mutate):
        tri_index = r.randrange(0, len(out))
        iterate = out[tri_index][:-int(target_image[2])] if element_color_locked else out[tri_index]
        if warp and r.random() <= warp_chance:
            for i, v in enumerate(iterate):
                newv = r.random()
                out[tri_index][i] = newv
        else:
            for i, v in enumerate(iterate):
                newv = v+r.uniform(-intensity, intensity)
                if newv < 0.0: newv = 0.0
                elif newv > 1.0: newv = 1.0
                out[tri_index][i] = newv
    return out

def random_dna():
    return new_dna()
    
def basic_dna():
    return new_dna()

def new_dna():
    if use_gene is None:
        out = []
        add_new_obs(tris, out)
    else:
        out = [x[:] for x in use_gene]
        if resize_arrays:
            if len(out) < tris:
                add_new_obs(tris-len(out), out)
            elif len(out) > tris:
                out = out[:-(len(out)-tris)]
    return out

def add_new_obs(num, out):
    for t in xrange(num):
        tri = []
        num_to_extend = drawmode2num[draw_mode]
        tri.extend(getStartXY(num_to_extend))
        for i in xrange(target_image[2]):
            tri.append(r.uniform(start_element_color_min[i], start_element_color_max[i]))
        out.append(tri)
    return

def getStartXY(num):
    out = []
    x = r.uniform(start_element_range[0][0], start_element_range[0][1])
    y = r.uniform(start_element_range[1][0], start_element_range[1][1])
    for n in xrange(num):
        v = x + r.uniform(start_element_offset[0][0], start_element_offset[0][1])
        if v < 0.0: v = 0.0
        elif v > 1.0: v = 1.0
        out.append(v)
        v = y + r.uniform(start_element_offset[1][0], start_element_offset[1][1])
        if v < 0.0: v = 0.0
        elif v > 1.0: v = 1.0
        out.append(v)
    return out

def getStartY(num):
    out = []
    
    for n in xrange(num):
        
        out.append(v)
    return out

def report(report):
    global last_drawn
    print("GENERATION: " + str(report["generation"]))
    #print("PROGRESS: " + str(round(float(report["generation"])/float(report["termination_generation"]), 6)*100.0)+"%")
    print("TIME: " + str(report["time"]))
    print("RAW FITNESS: " + str(report["top_fitness"]))
    print("VALUES LEFT: " + str(max_fitness - report["top_fitness"]))
    print("NORMALIZED: " + str(report["top_fitness"] / max_fitness))
    fitnessx.append(report["generation"])
    fitnessy.append(report["top_fitness"])
    img = makeImage(report["top_object"])
    if last_drawn == 0 or ((report["top_fitness"] / last_drawn) >= history_after):
        print("DRAWING HISTORY")
        PNG.saveFile("history/"+str(report["generation"])+".png", img)
        last_drawn = report["top_fitness"]
    print("")
    return

st = GeneAlg.SelectionTypes.tourney_select
dt = GeneAlg.SelectionTypes.tourney_low_select
fill = GeneAlg.FillTypes.random_fill
gene = GeneAlg.make_gene(fitness, mate, mutate, random_dna, basic_dna, report = report)

#op = GeneAlg.make_options(st, (7,), dt, (7,), fill, (), 1.0, .00, .1)
#GA = GeneAlg.Algorithms.Pool(gene, op, 300)

op = GeneAlg.make_options(st, (1,), dt, (1,), fill, (), 1.0, .00, max_mutation_intensity)
GA = GeneAlg.Algorithms.HillClimb(gene, op)

#op = GeneAlg.make_options(st, (1,), dt, (1,), fill, (), 1.0, .00, 1.0)
#GA = GeneAlg.Algorithms.MultiHillClimb(gene, op)

#op = GeneAlg.make_options(st, (2,), dt, (2,), fill, (), 1.0, .00, .75)
#GA = GeneAlg.Algorithms.Community(gene, op, 15)

reportc = GeneAlg.make_criteria(None, report_every)
savec = GeneAlg.make_criteria(None, 2000)
termc = GeneAlg.make_criteria(int(hours_to_run*3600.0), None)

GA.run(reportc, savec, termc)
ab = GA.getBest()
im = makeImage(ab[1])
PNG.saveFile(output_image, im)

if output_pickle is not None:
    f = gzip.open(output_pickle, "w")
    cPickle.dump(ab[1], f)
    f.close()

#make a graph image
dg = PyRange.DataGraph1D(default_interp=PyRange.Interpolation.linear)

dg.setFromXY(fitnessx, fitnessy)
Draw1D.saveDataGraph1DFile("./tri_score.png", dg)
