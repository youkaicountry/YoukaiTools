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

from YoukaiTools import PyRange
from . import Create
from . import Modify
import math

#have this go on given image if provided?
def renderPath(path, width, height, image=None, position=(0, 0), backcolor=[0, 0, 0], pathcolor=[1.0, 1.0, 1.0]):
    rp = Create.newImage(width, height, backcolor) if image is None else image
    for p in path:
        d = p.getLength()
        samples = max(int(math.ceil(d * max((width, height))) *.75 ), 5) 
        ds = 1.0 / float(samples)
        nexti = ds
        nextv = p.getIValue(nexti)
        i = 0
        v = p.getIValue(i)
        for n in range(samples):
            Modify.drawLine(rp, int((v[0]*width)+position[0]), int((v[1]*height)+position[1]), int((nextv[0]*width)+position[0]), int((nextv[1]*height)+position[1]), pathcolor)
            #Modify.drawLine(rp, int((v[0]*width)+position[0]+.5), int((v[1]*height)+position[1]+.5), int((nextv[0]*width)+position[0]+.5), int((nextv[1]*height)+position[1]+.5), pathcolor)
            i = nexti
            v = nextv
            nexti = i + ds
            nextv = p.getIValue(nexti)
    return rp

#dic["char"] = ((sizex, sizey), path)
def loadFontPathFile(f):
    return

#returns rasterfont dic
def renderPathFontToRasterFont(pathfont, height, pathcolor=[1.0, 1.0, 1.0]):
    out = {}
    #form backcolor:
    backcolor = []
    for c in pathcolor:
        nc = 1.0 - c
        if nc == .5: nc = 0
        backcolor.append(nc)
    for c in pathfont:
        h = int(height * pathfont[c][0][0])
        w = int(height * pathfont[c][0][1])
        out[c] = renderPath(pathfont[c][1], w, h, backcolor=backcolor, pathcolor=pathcolor)
    return (out, backcolor)

def writeRasterFontOnImage(im, position, rasterfont, text, spacebetween=0):
    curpos = [position[0], position[1]]
    for c in text:
        Modify.overlay(im, rasterfont[0][c], curpos[0], curpos[1], ignorecolor=rasterfont[1])
        curpos[0] += rasterfont[0][c][0] + spacebetween
    return


def makeDefaultPathFont():
    size = (1.0, .6)
    out = {}
    
    p = ( ("line", (.05, .95), (.5, .05)), ("line", (.5, .05), (.95, .95)), ("line", (.1, .5), (.9, .5)) )
    s = __makeShape(p)
    out["A"] = (size, s)
    
    p = ( ("line", (.05, .05), (.05, .95)), ("bquad", (.05, .05), (1.2, .275), (.05, .5)), ("bquad", (.05, .5), (1.2, .725), (.05, .95)) )
    s = __makeShape(p)
    out["B"] = (size, s)
    
    p = (("bquad", (.95, .1), (-.2, .5), (.95, .9)), )
    s = __makeShape(p)
    out["C"] = (size, s)
    
    p = (("bquad", (.05, .1), (1.2, .5), (.05, .9)), ("line", (.05, .1), (.05, .9)))
    s = __makeShape(p)
    out["D"] = (size, s)
    
    p = (("bquad", (.75, .1), (.25, .5), (.75, .9)), )
    s = __makeShape(p)
    out["("] = (size, s)
    
    p = (("bquad", (.25, .1), (.75, .5), (.25, .9)), )
    s = __makeShape(p)
    out[")"] = (size, s)
    
    p = (("bquad", (.5, .1), (-.5, .5), (.5, .9)), ("bquad", (.5, .1), (1.5, .5), (.5, .9)), ("line", (.75, .25), (.25, .75) ) )
    s = __makeShape(p)
    out["0"] = (size, s)
    
    #p = ( ("line", (.5, .05), (.5, .95)), ("line", (.5, .05), (.35, .2)), ("line", (.15, .95), (.85, .95)) )
    p = ( ("line", (.5, .05), (.5, .95)), ("line", (.15, .95), (.85, .95)), ("line", (.5, .05), (.15, .25)) )
    #p = ( ("line", (.5, .05), (.5, .95)), ("line", (.5, .05), (.15, .25)), ("line", (.15, .95), (.85, .95)) )
    s = __makeShape(p)
    out["1"] = (size, s)
    
    p = ( ("bcubic", (.05, .05), (1.5, .05), (.06, .95), (.05, .95)), ("line", (.15, .95), (.85, .95)))
    s = __makeShape(p)
    out["2"] = (size, s)
    return out

def __makeLine(start, end):
    lp = PyRange.Paths.LinePath(start, end)
    return lp

def __makeBezierCurveQuadratic(start, handle, end):
    bp = PyRange.Paths.BezierCurveQuadratic(start, handle, end)
    return bp

def __makeBezierCurveCubic(start, handle1, handle2, end):
    bp = PyRange.Paths.BezierCurveCubic(start, handle1, handle2, end)
    return bp

def __makeContainerPath(pieces):
    cp = PyRange.Paths.ContainerPath()
    for p in pieces:
        cp.addPiece(p, (0, 0))
    return cp

def __makeShape(components):
    pieces = []
    for c in components:
        if c[0] == "line":
            pieces.append(__makeLine(c[1], c[2]))
        elif c[0] == "bquad":
            pieces.append(__makeBezierCurveQuadratic(c[1], c[2], c[3]))
        elif c[0] == "bcubic":
            pieces.append(__makeBezierCurveCubic(c[1], c[2], c[3], c[4]))
    return pieces
    #return __makeContainerPath(pieces)
