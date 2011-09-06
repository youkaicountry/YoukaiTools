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

from YoukaiTools import GeneAlg
import testmath
import random

class test(GeneAlg.User.Gene):
    GA = 0
    x = 0
    
    def __init__(self):
        st = GeneAlg.SelectionTypes.TourneySelect(5)
        dt = GeneAlg.SelectionTypes.TourneyLowSelect(5)
        fill = GeneAlg.FillTypes.BasicFill(self)
        #fi = 

        op = GeneAlg.User.Options(st, dt, fill, .3, .00, .5)
        #self.GA = GeneAlg.Algorithms.Community(self, op, 30)
        self.GA = GeneAlg.Algorithms.Pool(self, op, 200)
    
    def getFitness(self, obj):
        return obj.fit()
    
    def mate(self, obj1, obj2):
        #print "mate"
        o = testmath.testmath(obj1.c)        
        r = random.randint(0, 1)
        if r == 0:
            o.a = obj1.a
        else:
            o.a = obj2.a
        r = random.randint(0, 1)
        if r == 0:
            o.b = obj1.b
        else:
            o.b = obj2.b
        return o
    
    def mutate(self, intensity, obj):
        #print "mutate"
        o = testmath.testmath(obj.c)
        o.a = obj.a
        o.b = obj.b
        r = random.randint(0, 1)
        if r == 0:
            o.a += intensity
        else:
            o.a -= intensity
        r = random.randint(0, 1)
        if r == 0:
            o.b += intensity
        else:
            o.b -= intensity
        return o
    
    def getRandom(self):
        o = testmath.testmath(1000)
        o.a = 1
        o.b = 1
        return o
        
    def getBasic(self):
        o = testmath.testmath(1000)
        o.a = 1
        o.b = 1
        return o
    

#FUND IT!
t = test()
t.GA.doGeneration(500000, 100)
ab = t.GA.getBest()
print ab
print ab[1].a
print ab[1].b
print ab[1].a + 2*ab[1].b 
raw_input("Press any key")