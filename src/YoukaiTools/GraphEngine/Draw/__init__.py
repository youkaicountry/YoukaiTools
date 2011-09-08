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

import YoukaiTools.GraphEngine.GraphTools.Data
from YoukaiTools import ImageTools
import YoukaiTools.ImageTools.FileHandlers.BMP
import YoukaiTools.ImageTools.FileHandlers.PNG
from YoukaiTools import PyRange

#TODO: Transition to specific pixel dimensions instead of dog multipliers

#["vertex", radius, color], ["edge", color]
#["vname", height, offset, vertexlist, color]

def drawSimple(g, imagename=None, locindices=("x", "y"), layers=[["edge", (None, (0, 0, 1.0))], ["vertex", .02, (None, (1.0, 0, 0))]], border=.05, smallwidth=256):
    xr = YoukaiTools.GraphEngine.GraphTools.Data.getVertexDataRange(g, locindices[0])
    yr = YoukaiTools.GraphEngine.GraphTools.Data.getVertexDataRange(g, locindices[1])
    xw = xr[1]-xr[0]
    yw = yr[1]-yr[0]
    
    textset = set(["vname"])
    for l in layers:
        if l[0] in textset:
            pathfont = ImageTools.LineFont.makeDefaultPathFont()
            break
    
    
    if xw < yw:
        width = int(smallwidth)
        height = int((yw/xw)*smallwidth)
    else:
        height = int(smallwidth)
        width = int((xw/yw)*smallwidth)
    image = ImageTools.Create.newImage(width, height, [0, 0, 0])
    bordersize = int(smallwidth*border)
    xir = (bordersize, width-bordersize)
    yir = (bordersize, height-bordersize)
    ploc = {}
    #make location lookup
    for v in g.getVertexList():
        p = []
        p.append(int(PyRange.Ranges.rangeToRange(g.getVertexData(v, locindices[0]), float(xr[0]), float(xr[1]), float(xir[0]), float(xir[1]))))
        p.append(int(PyRange.Ranges.rangeToRange(g.getVertexData(v, locindices[1]), float(yr[0]), float(yr[1]), float(yir[0]), float(yir[1]))))
        ploc[v] = p
    for layer in layers:
        if layer[0] == "vertex":
            radius = int(smallwidth*layer[1])
            for v in g.getVertexList():
                if layer[2][0] is None:
                    c = layer[2][1]
                else:
                    if layer[2][0] in g.getVertexDataKeys(v):
                        c = g.getVertexData(v, layer[2][0])
                    else:
                        c = layer[2][1]
                p = ploc[v]
                ImageTools.Modify.drawCircle(image, p[0], p[1], radius, c)
        elif layer[0] == "edge":
            for e in g.getEdgeList():
                ei = g.getEdgeInfo(e)
                p1 = ploc[ei[0]]
                p2 = ploc[ei[1]]
                if layer[1][0] is None:
                    c = layer[1][1]
                else:
                    if layer[1][0] in g.getEdgeDataKeys(e):
                        c = g.getEdgeData(e, layer[1][0])
                    else:
                        c = layer[1][1]
                ImageTools.Modify.drawLine(image, p1[0], p1[1], p2[0], p2[1], c)
        elif layer[0] == "vname":
            rasterfont = ImageTools.LineFont.renderPathFontToRasterFont(pathfont, layer[1], layer[4])
            vl = g.getVertexList() if layer[3] is None else layer[3]
            for v in vl:
                text = str(v)
                p = ploc[v]
                ImageTools.LineFont.writeRasterFontOnImage(image, (p[0]+layer[2][0], p[1]+layer[2][1]), rasterfont, text, 0)
        
    if imagename is not None:
        itype = imagename.split(".")[-1].lower()
        if itype == "png":
            ImageTools.FileHandlers.PNG.saveFile(imagename, image)
        elif itype == "bmp":
            ImageTools.FileHandlers.BMP.saveFile(imagename, image)
    return image
