from YoukaiTools import GraphEngine 
from YoukaiTools.GraphEngine.GraphTools.SpecialTypes import GridGraph
from YoukaiTools import ImageTools
from YoukaiTools.ImageTools.FileHandlers import BMP
from YoukaiTools.ImageTools.FileHandlers import PNG

import random

import sys

tolerance = .01

filename = sys.argv[1]
f = open(filename, "r")
ftype = filename.split(".")[-1].lower()
if ftype == "bmp":
    im = BMP.load(f)[0]
elif ftype == "png":
    im = PNG.load(f)[0]

bg = GraphEngine.BasicGraph()
points = []

vim = ImageTools.SubImage.averageChannels(im)
for y in range(vim[1]):
    for x in range(vim[0]):
        c = ImageTools.Metric.getColorAt(vim, x, y)
        if c[0] - tolerance < 0.0:
            points.append((x, y))

GridGraph.buildGridGraph(bg, points)

r = random.Random()
pedges = GraphEngine.GraphTools.Span.prim(bg, r=r)
pg = GraphEngine.Graphs.BasicGraph()
GraphEngine.GraphTools.SubGraph.copyGraph(pg, bg, edgelist=pedges)

GraphEngine.Draw.drawSimple(pg, "./output/image_maze.png", smallwidth=512, layers=[("edge", ("color", (0, 0, 1.0)))] )
