#Copyright (c) <2011-2012> <Nathaniel Caldwell>

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

#Functions that involve data

from YoukaiTools import AdvMath
from YoukaiTools import PyRange

#if vertexcolor or edgecolor are 
def setDataToPath(g, path, vertexdata=("color", (0, 1, 0)), edgedata=("color", (0, 1, 0))):
    for o in path:
        if vertexdata is not None:
            g.setVertexData(o[0], vertexdata[0], vertexdata[1])
        if o[1] is not None:
            if edgedata is not None:
                g.setEdgeData(o[1], edgedata[0], edgedata[1])
    return

def setVertexDataToAll(g, index, data, vertexids=None):
    if vertexids is None:
        vertexids = g.getVertexList()
    for v in vertexids:
        g.setVertexData(v, index, data)
    return

def setEdgeDataToAll(g, index, data, edgeids=None):
    if edgeids is None:
        edgeids = g.getVertexList()
    for v in edgeids:
        g.setEdgeData(v, index, data)
    return

def getVertexDataRange(g, index, vertexids=None):
    if vertexids is None:
        vertexids = g.getVertexList()
    low = AdvMath.POSITIVE_INFINITY
    high = AdvMath.NEGATIVE_INFINITY
    for v in vertexids:
        if index in g.getVertexDataKeys(v):
            vd = g.getVertexData(v, index)
            if vd < low: low = vd
            if vd > high: high = vd
    return (low, high)

def normalizeVertexData(g, index, vertexids=None, nrange=(0.0, 1.0), lohi=None):
    if vertexids is None:
        vertexids = g.getVertexList()
    if lohi is None:
        low, high = getVertexDataRange(g, index, vertexids)
    else:
        low, high = lohi
    for v in vertexids:
        vd = g.getVertexData(v, index)
        nvd = PyRange.Ranges.rangeToRange(vd, low, high, nrange[0], nrange[1])
        g.setVertexData(v, index, nvd)
    return

def normalizeDoubleVertexData(g, indices, vertexids=None, smallrange=(0,0, 1.0)):
    if vertexids is None:
        vertexids = g.getVertexList()
    low1, high1 = getVertexDataRange(g, indices[0], vertexids)
    low2, high2 = getVertexDataRange(g, indices[1], vertexids)
    print(low1, high1)
    print(low2, high2)
    d1 = (high1-low1)
    d2 = (high2-low2)
    if d1 < d2:
        r1 = smallrange
        r2 = [smallrange[0]]
        n = d2 / d1
        r2.append(smallrange[0] + n*d1)
    else:
        r2 = smallrange
        r1 = [smallrange[0]]
        n = d1 / d2
        r1.append(smallrange[0] + n*d2)
    normalizeVertexData(g, indices[0], vertexids, r1, (low1, high1))
    normalizeVertexData(g, indices[1], vertexids, r2, (low2, high2))
    return

def normalizeEdgeData(g, index, edgeids=None, nrange=(0.0, 1.0)):
    if edgeids is None:
        edgeids = g.getEdgeList()
    low = AdvMath.POSITIVE_INFINITY
    high = AdvMath.NEGATIVE_INFINITY
    for v in edgeids:
        vd = g.getEdgeData(v, index)
        if vd < low: low = vd
        if vd > high: high = vd
    for v in edgeids:
        vd = g.getEdgeData(v, index)
        nvd = PyRange.Ranges.rangeToRange(vd, low, high, nrange[0], nrange[1])
        g.setEdgeData(v, index, nvd)
    return
    
