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

import YoukaiTools.ImageTools as ImageTools

def fPoint(obj):
    return ((obj,),)

def toImageSpace(val, min, div, scale):
    return int(((val - min) / div) * scale)

#filter out objects if already drawn
#have function determine color
def drawQuadTree(quadtree, image_size=(256,256), back_color=(0.0,0.0,0.0), draw_nodes=True, node_color=(1.0,1.0,1.0), draw_objects=False, object_color=(1.0,0.0,0.0), object_point_function=fPoint):
    root = quadtree.root
    im = ImageTools.Create.newImage(image_size[0], image_size[1], back_color)
    region = quadtree.getNodeRegion(root)
    xmin = float(region[0])
    xdiv = float(region[2]-region[0])
    xscale = float(image_size[0]) - 1.0
    ymin = float(region[1])
    ydiv = float(region[3]-region[1])
    yscale = float(image_size[1]) - 1.0
    for n in quadtree.nodes:
        if n not in quadtree.leafnodes:
            if draw_nodes:
                r = quadtree.getNodeRegion(n)
                xp = toImageSpace((r[0]+r[2]) / 2.0, xmin, xdiv, xscale)
                yp = toImageSpace((r[1]+r[3]) / 2.0, ymin, ydiv, yscale)
                x0 = toImageSpace(r[0], xmin, xdiv, xscale)
                x1 = toImageSpace(r[2], xmin, xdiv, xscale)
                y0 = toImageSpace(r[1], ymin, ydiv, yscale)
                y1 = toImageSpace(r[3], ymin, ydiv, yscale)
                ImageTools.Modify.drawLine(im, xp, y0, xp, y1, node_color)
                ImageTools.Modify.drawLine(im, x0, yp, x1, yp, node_color)
        else:
            if draw_objects:
                for c in quadtree.nodes[n].objectcontainers:
                    obs = object_point_function(c[0])
                    for l in obs:
                        if len(l) == 1:
                            xp = toImageSpace(l[0][0], xmin, xdiv, xscale)
                            yp = toImageSpace(l[0][1], ymin, ydiv, yscale)
                            ImageTools.Modify.pset(im, xp, yp, object_color)
                        elif len(l) == 2:
                            x0 = toImageSpace(l[0][0], xmin, xdiv, xscale)
                            y0 = toImageSpace(l[0][1], ymin, ydiv, yscale)
                            x1 = toImageSpace(l[1][0], xmin, xdiv, xscale)
                            y1 = toImageSpace(l[1][1], ymin, ydiv, yscale)
                            ImageTools.Modify.drawLine(im, x0, y0, x1, y1, node_color)
    return im
