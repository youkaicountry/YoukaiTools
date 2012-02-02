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

import random
import itertools
from bisect import bisect

class AdvRandom:
    def __init__(self, r=None):
        if r is None:
            self.r = random.Random()
        else:
            self.r = r
        return
        
    def biasedChoice(self, seq, probseq=None):
        #Chooses an element from seq at random
        #Probability of each element given in probseq
        if probseq is None:
            probseq = itertools.repeat(1.0)
        total = sum(p for e,p in zip(seq, probseq))
        r = random.uniform(0.0, total)
        for e,p in zip(seq, self.__partialsum(probseq)):
            if p >= r:
                return e
        raise RuntimeError("Could not find element (total="+str(total)+", r="+str(r))
    
    def distribution(self, dist_func):
        return dist_func(self.r.random())
        
    def __partialsum(self, seq):
        total = 0.0
        for x in seq:
            total += x
            yield total
        return
        
_inst = AdvRandom()
biasedChoice = _inst.biasedChoice

class BiasedChoice():
    def __init__(self, sequence, probabilities=None, r=None):
        if probabilities is None:
            probabilities = [1 for x in sequence]
        if r is None:
            r = random.Random()
        self.r = r
        psum = float(sum([x for x in probabilities]))
        pseq = [float(x)/psum for x in probabilities]
        self.prob = []
        adder = 0
        for x in pseq:
            self.prob.append(x+adder)
            adder += x
        self.seq = sequence
        return
    
    def getChoice(self):
        i = bisect(self.prob, self.r.random())
        return self.seq[i]

    def getChoiceIndex(self):
        return bisect(self.prob, self.r.random())
        