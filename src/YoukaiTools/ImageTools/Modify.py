import YoukaiTools.AdvMath.Indices
from YoukaiTools import PyRange
from . import CombineFunctions
from . import Metric

#puts the over_image at x, y on the under_image 
#have combine function later
#OPTIMIZE: PRECALCULATE OX AND OY
#OPTIMIZE: CALCULATE PART OF OVER IMAGE IN BOUNDARIES AND ONLY DO THAT
def overlay(under_image, over_image, x, y, combine=CombineFunctions.paint, cparams=[], ignorecolor=None):
    #print(under_image)
    for oy in range(over_image[1]):
        #if oy + y < 0: continue
        #if oy + y > under_image[1]-1: continue
        for ox in range(over_image[0]):
            #if ox + x < 0: continue
            #if ox + x > under_image[1]-1: continue
            ui = YoukaiTools.AdvMath.Indices.arrayIndex2To1(ox+x, oy+y, under_image[0], 3)
            oi = YoukaiTools.AdvMath.Indices.arrayIndex2To1(ox, oy, over_image[0], 3)
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
    for oy in range(image[1]):
        for ox in range(image[0]):
            v = Metric.getColorAt
    return

def invertImage(image, channels=None, minv=0, maxv=1.0):
    if channels is None:
        channels = []
        for i in range(image[2]):
            channels.append(i)
    for oy in range(image[1]):
        for ox in range(image[0]):
            i = YoukaiTools.AdvMath.Indices.arrayIndex2To1(ox, oy, image[0], 3)
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
        for i in range(image[2]):
            channels.append(i)
    if sameinrange:
        inmin = ()
        inmax = None
        for oy in range(image[1]):
            for ox in range(image[0]):
                i = YoukaiTools.AdvMath.Indices.arrayIndex2To1(ox, oy, image[0], 3)
                for ch in channels:
                    if inmin > image[i][ch]: inmin = image[i][ch]
                    if inmax < image[i][ch]: inmax = image[i][ch]
        fmin = []
        fmax = []
        for t in range(len(channels)):
            fmin.append(inmin)
            fmax.append(inmax)
    else:
        inmin = []
        inmax = []
        for t in range(len(channels)):
            inmin.append(())
            inmax.append(None)
        for oy in range(image[1]):
            for ox in range(image[0]):
                i = YoukaiTools.AdvMath.Indices.arrayIndex2To1(ox, oy, image[0], 3)
                for i, ch in enumerate(channels):
                    if inmin[i] > image[i][ch]: inmin[i] = image[i][ch]
                    if inmax[i] < image[i][ch]: inmax[i] = image[i][ch]
        fmin = inmin
        fmax = inmax
    for oy in range(image[1]):
        for ox in range(image[0]):
            i = YoukaiTools.AdvMath.Indices.arrayIndex2To1(ox, oy, image[0], 3)
            for j, ch in enumerate(channels):
                image[i][j] = PyRange.rangeToRange(image[i][j], fmin[j], fmax[j], minv[j], maxv[j])
    return

def pset(image, x, y, color, combine=CombineFunctions.paint, cparams=[]):
    i = YoukaiTools.AdvMath.Indices.arrayIndex2To1(x, y, image[0], 3)
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

def drawLine(image, x0, y0, x1, y1, color, combine=CombineFunctions.paint, cparams=[]):
    print(x0, y0, x1, y1, color)
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
    pset(image, x0, y0, color, combine, cparams)
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
