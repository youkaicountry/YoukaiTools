#Copyright (c) <2011> <Nathaniel Caldwell>

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

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
