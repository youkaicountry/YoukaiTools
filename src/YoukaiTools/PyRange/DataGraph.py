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

import bisect
from math import floor, log

from .. import LineLoader

from . import Interpolation
from . import Extrapolation
from . import Ranges

#monotonic test:
#give number of vals in, and if 0's in
#returns monotonic, purely monotonic
mono = {}
mono[(0, True)] = (True, False)
mono[(1, False)] = (True, True)
mono[(1, True)] = (True, False)
mono[(2, False)] = (False, False)
mono[(2, True)] = (False, False)

class DataGraph1D:
    def __init__(self, default_interp=Interpolation.linear, default_extrap=Extrapolation.linear, default_tension=0, default_bias=0):
        self.xvalues = None
        self.yvalues = None
        self.fdomain = (0, 0)
        self.frange = (0, 0)
        self.monotonic = None
        self.puremonotonic = None
        self.yneighbors = {}
        self.xneighbors = {}
        self.minima = []
        self.maxima = []
        self.default_interp=default_interp
        self.default_tension=default_tension
        self.default_bias=default_bias
        self.default_extrap=default_extrap
        self.__i2g = {}
        self.__i2g[Interpolation.linear] = self.__ISingle
        self.__i2g[Interpolation.cosine] = self.__ISingle
        self.__i2g[Interpolation.quadratic] = self.__ISingle
        self.__i2g[Interpolation.cubic] = self.__ITriple
        self.__i2g[Interpolation.hermite] = self.__ITriple
        self.__i2g[Interpolation.catmullRom] = self.__ITriple
    
    def setFromFile(self, f):
        l = LineLoader.loadLines(f)
        self.setFromStringList(l)
        return
        
    def saveToFile(self, f):
        o = "\n".join([str(self.xvalues[i]) + " " + str(self.yvalues[i]) for i in range(len(self.xvalues))])
        f.writelines(o)
        return
    
    #string list ["10 12", "1.2 15", ...]
    def setFromStringList(self, sl):
        use = []
        nl = [x.split() for x in sl]
        for o in nl:
            p = (float(o[0]), float(o[1]))
            use.append(p)
        self.setFromPoints(use)
        return
    
    def setFromPoints(self, points, statistics=True):
        sp = sorted(points)
        xv = []
        yv = []
        for x in sp:
            xv.append(x[0])
            yv.append(x[1])
        self.setFromXY(xv, yv, statistics)
        return
    
    def setFromXY(self, xvalues, yvalues, statistics=True):
        self.xvalues = xvalues
        self.yvalues = yvalues
        self.monotonic = None
        self.puremonotonic = None
        self.__i2g = {}
        self.__i2g[Interpolation.linear] = self.__ISingle
        self.__i2g[Interpolation.cosine] = self.__ISingle
        self.__i2g[Interpolation.quadratic] = self.__ISingle
        self.__i2g[Interpolation.cubic] = self.__ITriple
        self.__i2g[Interpolation.hermite] = self.__ITriple
        self.__i2g[Interpolation.catmullRom] = self.__ITriple
        if statistics:
            self.fdomain = (self.xvalues[0], self.xvalues[-1])
            self.frange = (min(yvalues), max(yvalues))
            self.__getMonotonic()
            self.yneighbors = {}
            self.xneighbors = {}
            self.__getNeighbors()
            self.__getRegions()  
            self.__getMinimaMaxima()
        return
    
    def getXValue(self, index):
        return self.xvalues[index]
        
    def getYValue(self, index):
        return self.yvalues[index]
        
    def getLength(self):
        return len(self.xvalues)
    
    def getDomain(self):
        return self.fdomain
        
    def inDomain(self, value):
        if value >= self.fdomain[0] and value <= self.fdomain[1]: return True
        return False
        
    def getRange(self):
        return self.frange
        
    def inRange(self, value):
        if value >= self.frange[0] and value <= self.frange[1]: return True
        return False
        
    def isMonotonic(self):
        return self.monotonic
        
    def isPurelyMonotonic(self):
        return self.puremonotonic
    
    def getCenteredResample(self, samples, xr=None, interp=None, tension=None, bias=None):
        return self.getResample(samples, xr, 1, 1, 1, 1, interp, tension, bias)
    
    def getFramedResample(self, samples, xr=None, interp=None, tension=None, bias=None):
        return self.getResample(samples, xr, 0, 0, -1, 1, interp, tension, bias)
        
    def getResample(self, samples, xr=None, addsadd=1, addmul=1, dxsadd=1, dxmul=1, interp=None, tension=None, bias=None):
        outputx = []
        outputy = []
        if xr is None:
            uxr = self.fdomain
        else:
            uxr = xr
        le = uxr[1] - uxr[0]
        add = (le/float(samples+addsadd))*addmul
        dx = (float(le)/float(samples+dxsadd))*dxmul
        for i in range(samples):
            x = uxr[0] + (i*dx) + add
            y = self.getValue(x, interp, tension, bias)
            outputx.append(x)
            outputy.append(y)
        return (outputx, outputy)

    #outputs (points, xaxis, yaxis)
    def getGraphPrint(self, xslices, yslices, xr=None, yr=None, clip=True, interp=None, tension=None, bias=None):
        output = []
        if xr is None:
            uxr = self.fdomain
        else:
            uxr = xr
        if yr is None:
            uyr = self.frange
        else:
            uyr = yr
        for i in range(xslices):
            x = Ranges.rangeToRange(i, 0, xslices-1, uxr[0], uxr[1])
            y = self.getValue(x, interp, tension, bias)
            ycoord = Ranges.rangeToRange(y, uyr[0], uyr[1], 0, yslices-1)
            ycoord = floor(((yslices-1) - ycoord)+.5)
            if ycoord >= yslices or ycoord < 0: 
                if clip: continue
            output.append((i, ycoord))
        yaxis = Ranges.rangeToRange(0, uxr[0], uxr[1], 0, xslices-1)
        if yaxis > xslices-1 or yaxis < 0: yaxis = None
        xaxis = floor(((yslices-1)-Ranges.rangeToRange(0, uyr[0], uyr[1], 0, yslices-1))+.5)
        if xaxis > yslices-1 or xaxis < 0: xaxis = None
        return (output, xaxis, yaxis)
        
    def getInverse(self, statistics=True):
        if not self.puremonotonic: return None
        il = [(self.yvalues[i], self.xvalues[i]) for i in range(self.getLength())]
        il.sort()
        nx = [x[0] for x in il]
        ny = [x[1] for x in il]
        dg = DataGraph1D()
        dg.setFromXY(nx, ny)
        return dg
        
    def getValue(self, x, interp=None, tension=None, bias=None):
        if interp is None:
            interp = self.default_interp
        if bias is None:
            bias = self.default_bias
        if tension is None:
            tension=self.default_tension
        return self.__i2g[interp](x, interp, tension, bias)
        
    def __ISingle(self, x, interp, tension, bias):
        if x <= self.xvalues[0]: return Extrapolation.linear(x, self.xvalues[0], self.yvalues[0], self.xvalues[1], self.yvalues[1])
        if x >= self.xvalues[-1]: return Extrapolation.linear(x, self.xvalues[-2], self.yvalues[-2], self.xvalues[-1], self.yvalues[-1])
        ui = bisect.bisect(self.xvalues, x)
        mu = Ranges.normalize(x, self.xvalues[ui-1], self.xvalues[ui])
        return interp(float(mu), self.yvalues[ui-1], self.yvalues[ui])
        
    def __ITriple(self, x, interp, tension, bias):
        if x <= self.xvalues[0]: return Extrapolation.linear(x, self.xvalues[0], self.yvalues[0], self.xvalues[1], self.yvalues[1])
        if x >= self.xvalues[-1]: return Extrapolation.linear(x, self.xvalues[-2], self.yvalues[-2], self.xvalues[-1], self.yvalues[-1])
        ui = bisect.bisect(self.xvalues, x)
        ys = self.yneighbors[ui]
        mu = Ranges.normalize(x, self.xvalues[ui-1], self.xvalues[ui])
        return interp(mu, ys[0], ys[1], ys[2], ys[3], tension, bias)
        
    def __getMonotonic(self):
        direction = set()
        numin = 0
        for x in range(1, len(self.yvalues)):
            t = self.yvalues[x] - self.yvalues[x-1]
            if t == 0:
                direction.add(0)
            else:
                direction.add(t/abs(t))
        if 1 in direction: numin+= 1
        if -1 in direction: numin+= 1
        self.monotonic, self.puremonotonic = mono[(numin, 0 in direction)]
        return
        
    def __getNeighbors(self):
        for i in range(1, len(self.xvalues)):
            x1 = self.xvalues[i-1]
            y1 = self.yvalues[i-1]
            x2 = self.xvalues[i]
            y2 = self.yvalues[i]
            xs = x1 - (x2 - x1)
            if i <= 1:
                extrap = (x1, y1, x2, y2)
            else:
                x0t = self.xvalues[i-2]
                y0t = self.yvalues[i-2]
                extrap = (x0t, y0t, x1, y1)
            y0 = Extrapolation.linear(xs, *extrap)
            x0 = xs
            
            xs = x2 + (x2 - x1)
            if i >= self.getLength() - 1:
                extrap = (x1, y1, x2, y2)
            else:
                x3t = self.xvalues[i+1]
                y3t = self.yvalues[i+1]
                extrap = (x2, y2, x3t, y3t)
            y3 = Extrapolation.linear(xs, *extrap)
            x3 = xs
            self.yneighbors[i] = (y0, y1, y2, y3)
            self.xneighbors[i] = (x0, x1, x2, x3)
        return
    
    #regions are stored in terms of index, not value
    def __getRegions(self):
        reg = []
        for i in range(len(self.xvalues)-1):
            v = self.yvalues[i+1] - self.yvalues[i]
            reg.append([i, i+1, v/abs(v) if v != 0 else v])
        rstart = 0
        rsymb = reg[0][2]
        rcombine = []
        for i in range(1, len(reg)):
            if reg[i][2] != rsymb:
                rcombine.append([reg[rstart][0], reg[i][0], rsymb])
                rstart = i
                rsymb = reg[i][2]
        rcombine.append([reg[rstart][0], reg[len(reg)-1][1], rsymb])
        self.regions = rcombine
        return
    
    #needs regions to have been calculated already
    #Is tentatively working. Might need case tested
    #maxima and minima are stored in terms of index, not value
    def __getMinimaMaxima(self):
        minima = []
        maxima = []
        #add START
        if self.regions[0][2] == -1:
            maxima.append(self.regions[0][0])
        elif self.regions[0][2] == 1:
            minima.append(self.regions[0][0])
        else: #it is flat, then
            if self.regions[1][2] == -1:
                maxima.append(int((float(self.regions[0][0])+float(self.regions[0][1]))/2.0))
            else:
                minima.append(int((float(self.regions[0][0])+float(self.regions[0][1]))/2.0))
        for i in range(len(self.regions)):
            if self.regions[i][2] == -1:
                minima.append(self.regions[i][1])
            elif self.regions[i][2] == 1:
                maxima.append(self.regions[i][1])
            else: #it is flat, then
                if self.regions[i][2] == -1:
                    minima.append(int((float(self.regions[i][0])+float(self.regions[i][1]))/2.0))
                else:
                    maxima.append(int((float(self.regions[i][0])+float(self.regions[i][1]))/2.0))
        self.minima = minima
        self.maxima = maxima
        return
    
class PeriodicDataGraph1D:
    def __init__(self, dgraph1d, xscale=1.0, ytranslation=0.0):
        self.graph = dgraph1d
        self.xscale = xscale
        self.ytranslation = ytranslation
        return
    
    def getValue(self, x, interp=Interpolation.cosine, tension=0, bias=0):
        domain = self.graph.getDomain()
        nx = Ranges.rangeToRange(x, domain[0], domain[1], 1.0, 2.0)
        if self.xscale == 1.0:
            N = floor(nx)
            norm = Ranges.normalize(nx, N, N+1)
            EN = N-1
        else:
            N = floor(log(nx) / log(self.xscale))
            norm = Ranges.normalize(nx, pow(self.xscale, N), pow(self.xscale, N+1))
            EN = N
        #print(N)
        val = Ranges.rangeToRange(norm, 0.0, 1.0, domain[0], domain[1])
        y = self.graph.getValue(val, interp, tension, bias) + (self.ytranslation*EN)
        return y
