import random
from math import pi, sin, cos
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
from YoukaiTools.AdvRandom import BiasedChoice
from YoukaiTools.AdvMath.Statistics import mean

fitnessx = []
fitnessy = []

ur = random.Random()
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
tris = 1000
#Whether to resize laoded arrays or not
resize_arrays = True
#The maximum mutation intensity
max_mutation_intensity = .2

change_location_chance = 1
change_color_chance = 1
change_both_chance = 1

jostle_location_chance = 2
jostle_single_point_chance = 2
translate_chance = 2
scale_chance = 2
rotate_chance = 2
warp_chance = 1

jostle_color_chance = 2
warp_color_chance = 1
jostle_single_color_value_chance = 2

max_translate_amount = .2
max_scale_amount = .25
max_rotate_amount = pi
max_jostle_amount = .2

max_jostle_color_amount = .2

#The maximum number of mutations to attempt each cycle
max_mutates = 4
#The mix method to use for painting
mix_method = "multiply"
#Number of hours to run the simulation
hours_to_run = 3.0
#Report every how many generations?
report_every = 50
#draw after an improvement of:
history_after = 1.0005

draw_mode = "line" #line or triangle

start_element_color_min = [1.0, 1.0, 1.0]
start_element_color_max = [1.0, 1.0, 1.0]
start_background_color = [1.0, 1.0, 1.0]
start_element_range = ((0.0, 1.0), (0.0, 1.0))
#start_element_offset = ((-1.0, 1.0), (-1.0, 1.0))
start_element_offset = ((-.2, .2), (-.2, .2))
# --------

action_bc = BiasedChoice(["location", "color", "both"], [change_location_chance, change_color_chance, change_both_chance])
loc_bc = BiasedChoice(["jostle_location", "jostle_single_point", "translate", "scale", "rotate", "warp"], [jostle_location_chance, jostle_single_point_chance, translate_chance, scale_chance, rotate_chance, warp_chance])
color_bc = BiasedChoice(["jostle_color", "warp_color", "jostle_single_color_value"], [jostle_color_chance, warp_color_chance, jostle_single_color_value_chance])

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

def fitness(obj, r):
    img = makeImage(obj)
    f = ImageTools.Comparison.manhattanDistance(img, target_image)
    return max_fitness - f

def mate(obj1, obj2, r):
    a = [obj1, obj2]
    return a[r.randint(0, 1)]

def mutate(intensity, obj, r):
    out = [x[:] for x in obj]
    to_mutate = min(max((int(len(obj)*intensity), 1)), max_mutates)
    #if to_mutate < 1: to_mutate = 1
    for n in xrange(to_mutate):
        tri_index = r.randrange(0, len(out))
        #iterate = out[tri_index][:-int(target_image[2])] if element_color_locked else out[tri_index]
        action = action_bc.getChoice()
        if action == "location":
            change_location(out, tri_index, r)
            normalize_values(out, tri_index)
        elif action == "color":
            change_color(out, tri_index, r)
            normalize_values(out, tri_index)
        elif action == "both":
            change_location(out, tri_index, r)
            change_color(out, tri_index, r)
            normalize_values(out, tri_index)
    return out

def change_location(obj, index, r):
    loc2func[loc_bc.getChoice()](obj, index, r)
    return

def change_color(obj, index, r):
    color2func[color_bc.getChoice()](obj, index, r)
    return

def jostle_location(obj, index, r):
    n = get_loc_num(obj, index)
    for i in xrange(n/2):
        ui = i*2
        obj[index][ui] = obj[index][ui]+r.uniform(-max_jostle_amount, max_jostle_amount)
        obj[index][ui+1] = obj[index][ui+1]+r.uniform(-max_jostle_amount, max_jostle_amount)
    return

def jostle_single_point(obj, index, r):
    n = get_loc_num(obj, index)
    point = r.randint(0, (n/2)-1)
    obj[index][point] = obj[index][point]+r.uniform(-max_jostle_amount, max_jostle_amount)
    obj[index][point+1] = obj[index][point+1]+r.uniform(-max_jostle_amount, max_jostle_amount)
    return

def translate(obj, index, r):
    n = get_loc_num(obj, index)
    translate_x = r.uniform(-max_translate_amount, max_translate_amount)
    translate_y = r.uniform(-max_translate_amount, max_translate_amount)
    for i in xrange(n/2):
        ui = i*2
        obj[index][ui] = obj[index][ui] + translate_x
        obj[index][ui+1] = obj[index][ui+1] + translate_y
    return

def scale(obj, index, r):
    n = get_loc_num(obj, index)
    center = find_center(obj, index, n)
    scale_factor = 1.0 + r.uniform(-max_scale_amount, max_scale_amount)
    for i in xrange(n/2):
        ui = i*2
        obj[index][ui] = ((obj[index][ui] - center[0]) * scale_factor) + center[0]
        obj[index][ui+1] = ((obj[index][ui+1] - center[1]) * scale_factor) + center[1]
    return

def rotate(obj, index, r):
    n = get_loc_num(obj, index)
    center = find_center(obj, index, n)
    rotation = r.uniform(-max_rotate_amount, max_rotate_amount)
    for i in xrange(n/2):
        ui = i*2
        xo = obj[index][ui] - center[0]
        yo = obj[index][ui+1] - center[1]
        obj[index][ui] = (xo*cos(rotation) - yo*sin(rotation)) + center[0]
        obj[index][ui+1] = (yo*cos(rotation) + xo*sin(rotation)) + center[1]
    return

def warp(obj, index, r):
    n = get_loc_num(obj, index)
    for i in xrange(n):
        obj[index][i] = r.random()
    return

def jostle_color(obj, index, r):
    for i in xrange(target_image[2]):
        ui = -(i+1)
        obj[index][ui] = obj[index][ui]+r.uniform(-max_jostle_amount, max_jostle_amount)
    return

def warp_color(obj, index, r):
    for i in xrange(target_image[2]):
        ui = -(i+1)
        obj[index][ui] = r.random()
    return

def jostle_single_color_value(obj, index, r):
    ui = -(r.randint(0, target_image[2])+1)
    obj[index][ui] = obj[index][ui]+r.uniform(-max_jostle_amount, max_jostle_amount)
    return

def get_loc_num(obj, index):
    return len(obj[index])-target_image[2]

def find_center(obj, index, n):
    values = obj[index][:n]
    return (mean(values[::2]), mean(values[1::2]))

def normalize_values(obj, index):
    for i in xrange(len(obj[index])):
        newv = obj[index][i]
        if newv < 0.0: newv = 0.0
        elif newv > 1.0: newv = 1.0
        obj[index][i] = newv
    return

color2func = {}
color2func["jostle_color"] = jostle_color
color2func["warp_color"] = warp_color
color2func["jostle_single_color_value"] = jostle_single_color_value

loc2func = {}
loc2func["jostle_location"] = jostle_location
loc2func["jostle_single_point"] = jostle_single_point
loc2func["translate"] = translate
loc2func["scale"] = scale
loc2func["rotate"] = rotate
loc2func["warp"] = warp

def generate(r):
    return new_dna(r)

def new_dna(r):
    if use_gene is None:
        out = []
        add_new_obs(tris, out, r)
    else:
        out = [x[:] for x in use_gene]
        if resize_arrays:
            if len(out) < tris:
                add_new_obs(tris-len(out), out, r)
            elif len(out) > tris:
                out = out[:-(len(out)-tris)]
    return out

def add_new_obs(num, out, r):
    for t in xrange(num):
        tri = []
        num_to_extend = drawmode2num[draw_mode]
        tri.extend(getStartXY(num_to_extend, r))
        for i in xrange(target_image[2]):
            tri.append(r.uniform(start_element_color_min[i], start_element_color_max[i]))
        out.append(tri)
    return

def getStartXY(num, r):
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
gene = GeneAlg.make_gene(fitness, mate, mutate, generate, report = report)

#op = GeneAlg.make_options(st, (7,), dt, (7,), fill, (), 1.0, .00, .1)
#GA = GeneAlg.Algorithms.Pool(gene, op, 300)

op = GeneAlg.make_options(st, (1,), dt, (1,), 1.0, .00, max_mutation_intensity)
GA = GeneAlg.Algorithms.HillClimb(gene, op, r=ur)

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
