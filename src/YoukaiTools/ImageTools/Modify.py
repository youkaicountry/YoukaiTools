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

from YoukaiTools.AdvMath.Indices import arrayIndex2To1
from YoukaiTools import PyRange
Paths = PyRange.Paths

from . import CombineFunctions
from . import Metric

#puts the over_image at x, y on the under_image 
#have combine function later
#OPTIMIZE: PRECALCULATE OX AND OY
#OPTIMIZE: CALCULATE PART OF OVER IMAGE IN BOUNDARIES AND ONLY DO THAT
def overlay(under_image, over_image, x, y, combine=CombineFunctions.paint, cparams=[], ignorecolor=None):
    #print(under_image)
    for oy in xrange(over_image[1]):
        #if oy + y < 0: continue
        #if oy + y > under_image[1]-1: continue
        for ox in xrange(over_image[0]):
            #if ox + x < 0: continue
            #if ox + x > under_image[1]-1: continue
            ui = arrayIndex2To1(ox+x, oy+y, under_image[0], 3)
            oi = arrayIndex2To1(ox, oy, over_image[0], 3)
            #print(ignorecolor, over_image[oi])
            if over_image[oi] != ignorecolor: 
                under_image[ui] = combine(under_image[ui], over_image[oi], *cparams)
    return

def applyColor(image, color, combine=CombineFunctions.paint, cparams=[]):
    for i, c in enumerate(image[3:]):
        image[i+3] = combine(c, color, *cparams)
    return

#if same, clip if A
def clipImage(image, clipbottom, cliptop, channels=None, newbottom=None, newin=None, newtop=None):
    for oy in xrange(image[1]):
        for ox in range(image[0]):
            v = Metric.getColorAt
    return

def invertImage(image, channels=None, minv=0, maxv=1.0):
    if channels is None:
        channels = []
        for i in xrange(image[2]):
            channels.append(i)
    for oy in xrange(image[1]):
        for ox in xrange(image[0]):
            i = arrayIndex2To1(ox, oy, image[0], 3)
            for ch in channels:
                image[i][ch] = (maxv-image[i][ch])+minv
    return
    

#sameinrange=False : seperate old min/max per channel
#sameinrange=True  : same old min/max for all channels
#channels = [1, 3] or whatever channel indices to do
#minv & maxv = [0.0, 0.2] or whatever the min for each channel used and max for each channel used should be
def normalize(image, minv, maxv, channels=None, sameinrange=True):
    if channels is None:
        channels = []
        for i in xrange(image[2]):
            channels.append(i)
    if sameinrange:
        inmin = ()
        inmax = None
        for oy in xrange(image[1]):
            for ox in xrange(image[0]):
                i = arrayIndex2To1(ox, oy, image[0], 3)
                for ch in channels:
                    if inmin > image[i][ch]: inmin = image[i][ch]
                    if inmax < image[i][ch]: inmax = image[i][ch]
        fmin = []
        fmax = []
        for t in xrange(len(channels)):
            fmin.append(inmin)
            fmax.append(inmax)
    else:
        inmin = []
        inmax = []
        for t in xrange(len(channels)):
            inmin.append(())
            inmax.append(None)
        for oy in xrange(image[1]):
            for ox in xrange(image[0]):
                i = arrayIndex2To1(ox, oy, image[0], 3)
                for i, ch in enumerate(channels):
                    if inmin[i] > image[i][ch]: inmin[i] = image[i][ch]
                    if inmax[i] < image[i][ch]: inmax[i] = image[i][ch]
        fmin = inmin
        fmax = inmax
    for oy in xrange(image[1]):
        for ox in xrange(image[0]):
            i = arrayIndex2To1(ox, oy, image[0], 3)
            for j, ch in enumerate(channels):
                image[i][j] = PyRange.rangeToRange(image[i][j], fmin[j], fmax[j], minv[j], maxv[j])
    return

def pset(image, x, y, color, combine=CombineFunctions.paint, cparams=[]):
    i = arrayIndex2To1(x, y, image[0], 3)
    image[i] = combine(image[i], color, *cparams)
    return

def drawCircle(image, cx, cy, radius, color, combine=CombineFunctions.paint, cparams=[]):
    rerror = 0
    xchange = 1-2*radius
    ychange=1
    x = radius
    y = 0
    while x >= y:
        pset(image, cx+x, cy+y, color, combine, cparams)
        pset(image, cx-x, cy+y, color, combine, cparams)
        pset(image, cx-x, cy-y, color, combine, cparams)
        pset(image, cx+x, cy-y, color, combine, cparams)
        pset(image, cx+y, cy+x, color, combine, cparams)
        pset(image, cx-y, cy+x, color, combine, cparams)
        pset(image, cx-y, cy-x, color, combine, cparams)
        pset(image, cx+y, cy-x, color, combine, cparams)
        y+=1
        rerror+=ychange
        ychange+=2
        if (2*rerror + xchange) > 0:
            x-=1
            rerror+=xchange
            xchange+=2
    return

def drawLine(image, x0, y0, x1, y1, color, string=False, combine=CombineFunctions.paint, cparams=[]):
    #print(x0, y0, x1, y1, color)
    dy = y1 - y0
    dx = x1 - x0
    stepx = 0
    stepy = 0
    if dy < 0:
        dy = -dy
        stepy = -1
    else:
        stepy = 1
    if dx < 0:
        dx = -dx
        stepx = -1
    else:
        stepx = 1
    dy <<= 1
    dx <<= 1
    if not string: pset(image, x0, y0, color, combine, cparams)
    if dx > dy:
        fraction = dy - (dx >> 1) #2*dy - dx
        while x0 != x1:
            if fraction >= 0:
                y0 += stepy
                fraction -= dx
            x0 += stepx
            fraction += dy
            pset(image, x0, y0, color, combine, cparams)
    else:
        fraction = dx - (dy >> 1)
        while y0 != y1:
            if fraction >= 0:
                x0 += stepx
                fraction -= dy
            y0 += stepy
            fraction += dx
            pset(image, x0, y0, color, combine, cparams)
    return

def drawBox(image, topleftx, toplefty, width, height, color, combine=CombineFunctions.paint, cparams=[]):
    drawLine(image, topleftx, toplefty, topleftx+width, toplefty, color, combine, cparams)
    drawLine(image, topleftx, toplefty, topleftx, toplefty+height, color, combine, cparams)
    drawLine(image, topleftx+width, toplefty, topleftx+width, toplefty+height, color, combine, cparams)
    drawLine(image, topleftx, toplefty+height, topleftx+width, toplefty+height, color, combine, cparams)
    return

def drawHorizontalLine(image, x, y, size, color, combine=CombineFunctions.paint, cparams=[]):
        #print("LINE", x, y, size)
        xsize = image[0]
        ysize = image[1]
        if y > 0 and y < ysize and x < xsize:
        #clip left hand side of scan
            if x < 0:
                size += x
                x = 0
   
        #y = y * xsize + x;
        locx = x
        locy = y
        top = 0
   
        if x + size < xsize : top = locx + size;
        else : top = locx + size - (locx + size - xsize)
        
        for tx in xrange(locx, top):
            pset(image, tx, locy, color, combine, cparams)

def drawPath(image, path, color, pieces=None, combine=CombineFunctions.paint, cparams=[]):
    pl = path.getLength()
    if pieces is None:
        pieces = max(pl+1, 1.0)
    di = 1.0 / float(pieces)
    i = 0
    loc0 = path.getIValue(i)
    i+= di
    loc1 = path.getIValue(i)
    drawLine(image, int(loc0[0]), int(loc0[1]), int(loc1[0]), int(loc1[1]), color, False, combine, cparams)
    for n in xrange(1, pieces):
        loc0 = path.getIValue(i)
        i += di
        #pset(image, int(round(p[0])), int(round(p[1])), color, combine, cparams)
        loc1 = path.getIValue(i)
        drawLine(image, int(loc0[0]), int(loc0[1]), int(loc1[0]), int(loc1[1]), color, True, combine, cparams)
    return
    
def drawQuadraticBezier(image, p0, p1, p2, color, pieces=None, combine=CombineFunctions.paint, cparams=[]):
    qb = Paths.BezierCurveQuadratic(p0, p1, p2)
    drawPath(image, qb, color, pieces, combine, cparams)
    return

def drawCubicBezier(image, p0, p1, p2, p3, color, pieces=None, combine=CombineFunctions.paint, cparams=[]):
    cb = Paths.BezierCurveCubic(p0, p1, p2, p3)
    drawPath(image, cb, color, pieces, combine, cparams)
    return

def drawPolygon(image, points, color, combine=CombineFunctions.paint, cparams=[]):
    for n in xrange(len(points)-1):
        p0 = points[n]
        p1 = points[n+1]
        drawLine(image, p0[0], p0[1], p1[0], p1[1], color, combine, cparams)
    return

def drawFilledTriangle(image, xi1, yi1, xi2, yi2, xi3, yi3, color, combine=CombineFunctions.paint, cparams=[]):
        x0, y0, x1, y1, x2, y2 = __sortTri([ (yi1, xi1), (yi2, xi2), (yi3, xi3) ])
        
        d0  = 0
        d1  = 0
        d2  = 0
  
        dx0 = 0
        dx1 = 0
        dx2 = 0
  
        dy0 = 0
        dy1 = 0
        dy2 = 0
        
        dy = [0,0,0]
        d  = [0,0,0]

        dt = 0
        i = 0
        
        if y1 < y0 : dt = y0; y0 = y1; y1 = dt; dt = x0; x0 = x1; x1 = dt
        if y2 < y1 : dt = y1; y1 = y2; y2 = dt; dt = x1; x1 = x2; x2 = dt
        if y2 < y0 : dt = y0; y0 = y2; y2 = dt; dt = x0; x0 = x2; x2 = dt
        
        dx0 = x1 - x0
        dy0 = y1 - y0

        dx1 = x2 - x1
        dy1 = y2 - y1
  
        dx2 = x0 - x2
        dy2 = y0 - y2
        
        if dy0 != 0 : d0 = float(dx0) / float(dy0)
        else : d0 = 0
  
        if dy1 != 0 : d1 = float(dx1) / float(dy1)
        else : d1 = 0
  
        if dy2 != 0 : d2 = float(dx2) / float(dy2)
        else : d2 = 0
        
        sx = 0
        ex = 0
        id = 0
  
        for i in xrange(int(y0), int(y1)):
            id = float(i)
  
            sx = int(x0 + ((id - y0) * d2))
            ex = int(x0 + ((id - y0) * d0))
  
            if sx < ex : drawHorizontalLine(image, sx, i, ex - sx, color, combine, cparams)
            else : drawHorizontalLine(image, ex, i, sx - ex, color, combine, cparams)
  
        for i in xrange(int(y1), y2):
            sx = int(x0 + ((i - y0) * d2))
            ex = int(x1 + ((i - y1) * d1))
  
            if sx < ex : drawHorizontalLine(image, sx, i, ex - sx, color, combine, cparams)
            else : drawHorizontalLine(image, ex, i, sx - ex, color, combine, cparams)

def __sortTri(trilist):
        trilist.sort()
        return (trilist[0][1], trilist[0][0], trilist[1][1], trilist[1][0], trilist[2][1], trilist[2][0])
