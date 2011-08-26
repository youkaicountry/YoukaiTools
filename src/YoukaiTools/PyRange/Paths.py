import math
import bisect
from . import Ranges

class BasePath:
    def __init__(self):
        self.length = 0
        return
        
    def getLength(self):
        return self.length
        
    def getIValue(self, i):
        return
    
    def getDValue(self, d):
        return self.getIValue(d / self.getLength())
    
    def estimateLength(self, startsegments=100, tolerance=.001, cutoff=1):
        segments = startsegments
         
        ds = 1.0 / float(segments)
        nexti = ds
        nextv = self.getIValue(nexti)
        i = 0
        v = self.getIValue(i)
        adder = 0
        for n in range(segments):
            d = []
            for c in range(len(v)):
                dx = nextv[c] - v[c]
                d.append(dx*dx)
            adder += math.sqrt(sum(d))
            i = nexti
            v = nextv
            nexti = i + ds
            nextv = self.getIValue(nexti)
        return adder

class LinePath(BasePath):
    def __init__(self, start=(0,0), end=(1,1)):
        self.start = start
        self.end = end
        dx = end[0]-start[0]
        dy = end[1]-start[1]
        self.length = math.sqrt(dx*dx + dy*dy)
        return
    
    def getIValue(self, i):
        x = Ranges.rangeToRange(i, 0, 1.0, self.start[0], self.end[0])
        y = Ranges.rangeToRange(i, 0, 1.0, self.start[1], self.end[1])
        return (x, y)

#if ax and bx are both 0.... line? maybe?
class BezierCurveQuadratic(BasePath):
    def __init__(self, p0=(0, 0), p1=(.5, .5), p2=(1, 0)):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.length = self.__calcLength()
        return
    
    def getIValue(self, i):
        return (self.__getBValue(i, 0), self.__getBValue(i, 1))
    
    def __getBValue(self, i, index):
        #A = ((1-i)**2) * self.p0[index]
        #B = 2*(1-i)*i*self.p1[index]
        #C = (i*i)*self.p2[index]
        return ((1-i)**2) * self.p0[index] + 2*(1-i)*i*self.p1[index] + (i*i)*self.p2[index]
    
    def __calcLength(self):
        ax = self.p0[0] - 2*self.p1[0] + self.p2[0]
        ay = self.p0[1] - 2*self.p1[1] + self.p2[1]
        bx = 2*self.p1[0] - 2*self.p0[0]
        by = 2*self.p1[1] - 2*self.p0[1]
        A = 4*(ax*ax + ay*ay)
        B = 4*(ax*bx + ay*by)
        C = bx*bx + by*by
        Sabc = 2*math.sqrt(A+B+C)
        A_2 = math.sqrt(A)
        A_32 = 2*A*A_2
        C_2 = 2*math.sqrt(C)
        BA = B/A_2
        return ( A_32*Sabc + A_2*B*(Sabc-C_2) + (4*C*A-B*B)*math.log( (2*A_2+BA+Sabc)/(BA+C_2) ) )/(4*A_32)

#if ax and bx are both 0.... line? maybe?
class BezierCurveCubic(BasePath):
    def __init__(self, p0=(0, 0), p1=(0, .5), p2=(1, .5), p3=(1, 0)):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.length = self.estimateLength()
        self.q1 = 0
        self.q2 = 0
        self.q3 = 0
        self.q4 = 0
        self.q5 = 0
        return
    
    def getIValue(self, i):
        return (self.__getBValue(i, 0), self.__getBValue(i, 1))
    
    def __getBValue(self, i, index):
        return ((1-i)**3)*self.p0[index] + 3*i*((1-i)**2)*self.p1[index] + 3*i*i*(1-i)*self.p2[index] + (i**3) * self.p3[index]
    

class ContainerPath(BasePath):
    def __init__(self):
        self.pieces = []
        self.starts = []
        self.dpositions = []
        self.ipositions = []
        self.length = 0
        self.size = 0
        return
    
    #if start is none, it will offset the given path to the end of the last
    #path
    def addPiece(self, piece, offset=None):
        self.pieces.append(piece)
        if len(self.starts) == 0:
            if offset is None:
                self.starts.append((0, 0))
            else:
                self.starts.append(offset)
            self.dpositions.append(0)
            self.ipositions.append(0)
            self.length = piece.getLength()
        else:
            if offset is None:
                lastend = self.getIValue(1.0)
            else:
                lastend = offset
            self.starts.append(lastend)
            self.dpositions.append(self.length)
            self.ipositions.append(self.length/(self.length+piece.length))
            self.length += piece.length
        self.size += 1
        return
    
    def getIValue(self, i):
        #if self.size == 1:
        #    v = self.pieces[0].getIValue(i)
        #   return (self.starts[0][0]+v[0], self.starts[0][1]+v[1])
        index = bisect.bisect(self.ipositions, i)-1
        p = self.pieces[index]
        herei = self.ipositions[index]
        topi = 1.0 if index == self.size-1 else self.ipositions[index+1]
        ni = Ranges.normalize(i, herei, topi)
        v = p.getIValue(ni)
        s = self.starts[index]
        return (s[0]+v[0], s[1]+v[1])

    
