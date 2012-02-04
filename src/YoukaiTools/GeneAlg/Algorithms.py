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

import BaseGA

class Community(BaseGA.BaseGA):
    def __init__(self, genes, options, communitysize, savehistoryperiod=10000, maxhistorylength=10, r=None):
        BaseGA.BaseGA.__init__(self, genes, options, savehistoryperiod, maxhistorylength, r) #call super constructor
        self.communitysize = communitysize
        self.genelist = []
        self.need_sort = True
        o = []
        if self.options["seeds"] is not None:
            for x in self.options["seeds"]:
                self.genelist.append((self.genes["fitness"](x, self.r), x))
        left = communitysize - len(self.options["seeds"])
        if left < 0: left = 0
        for l in xrange(left):
            o.append(self.genes["generate"](self.r))
        for i in range(len(o)):
            self.genelist.append((self.genes["fitness"](o[i], self.r), o[i]))
        self.genelist.sort()        
            
        
    def doGeneration(self):
        oldlist = self.genelist
        self.genelist = []
        for j in xrange(self.communitysize):
            s1 = self.getSelectionNew(oldlist)
            s2 = self.getSelectionNew(oldlist)
            o = self.mateNew(oldlist[s1][1], oldlist[s2][1])
            f = self.mutateNew(o)
            self.genelist.append((self.genes["fitness"](f, self.r), f))

class Pool(BaseGA.BaseGA):
    def __init__(self, genes, options, poolsize, savehistoryperiod=10000, maxhistorylength=10, r=None):
        BaseGA.BaseGA.__init__(self, genes, options, savehistoryperiod, maxhistorylength, r)
        self.poolsize = poolsize
        self.genelist = []
        self.need_sort = True
        o = []
        if self.options["seeds"] is not None:
            for x in self.options["seeds"]:
                self.genelist.append((self.genes["fitness"](x, self.r), x))
        else:
            o.append(self.genes["generate"](self.r))
        for i in range(len(o)):
            self.genelist.append((self.genes["fitness"](o[i], self.r), o[i]))
        
    def doGeneration(self):
        s1 = self.getSelectionInPlace()
        s2 = self.getSelectionInPlace()
        o = self.mateInPlace(s1, s2)
        f = self.mutateNew(o)
        if len(self.genelist) < self.poolsize:
            self.genelist.append((self.genes["fitness"](f, self.r), f))
        else:
            d = self.getDeletionInPlace()
            self.genelist[d] = (self.genes["fitness"](f, self.r), f)

class HillClimb(BaseGA.BaseGA):
    def __init__(self, genes, options, savehistoryperiod=10000, maxhistorylength=10, r=None):
        BaseGA.BaseGA.__init__(self, genes, options, savehistoryperiod, maxhistorylength, r)
        self.genelist = []
        o = []
        self.need_sort = False
        if self.options["seeds"] is not None:
            s = self.options["seeds"][0]
            self.genelist.append((self.genes["fitness"](s, self.r), s))
        else:
            o.append(self.genes["generate"](self.r))
            self.genelist = [(self.genes["fitness"](o[0], self.r), o[0])]
    
    def doGeneration(self):
        o = self.mutateGeneListObject(0)
        fit = self.genes["fitness"](o, self.r)
        #print(fit, self.genelist[0][0])
        if fit >= self.genelist[0][0]:
            self.genelist[0] = (fit, o)
        return


# keeps some number of genes, each doing a hillclimb type procedure. Whenever one jumps, if the old fitness is higher than
# anything in experimental threads, then the lowest experimental is replaced with that.
# If an experimental ever jumps, if there is anything in the main list lower than it AND with greater time since jump, then they are switched.
class MultiHillClimb(BaseGA.BaseGA):
    def __init__(self, genes, options, savehistoryperiod=10000, maxhistorylength=10, threads=4, experimental_threads=3, mixupmult = 3, maxmixuptime=100000, r=None):
        BaseGA.BaseGA.__init__(self, genes, options, savehistoryperiod, maxhistorylength, r)
        self.need_sort = True
        self.genelist = []
        self.time_since_jump = []
        
        self.time_since_highest_jump = None
        self.last_highest = 0
        self.last_highest_time_ago = 0
        # if there was no jump in highest, add 1 to time_ago
        # if there was a jump, time since highest = time_ago, and time_ago = 0
        # if time ago is min (mult times last_highest, maxmixuptime):
        #     a mixup occurs:
        #     dumbly replace any main with an experimental that is higher than it.
        #     Take the now lowest experimental, and replace it with a straight mating
        o = []
        for i in xrange(threads):
            self.time_since_jump.append(0)
            if self.options["seeds"] is not None:
                s = self.options["seeds"][0]
                self.genelist.append((self.genes["fitness"](s, self.r), s))
            else:
                o.append(self.options["generate"]())
                self.genelist = [(self.genes["fitness"](o[0], self.r), o[0])]
        
        self.experimental_genelist = []
        self.experimental_time_since_jump = []
        for i in xrange(experimental_threads):
            self.experimental_genelist.append((0, None))
            self.experimental_time_since_jump.append(0)
        
    def doGeneration(self):
        for i in xrange(len(self.genelist)):
            o = self.mutateGeneListObject(i)
            fit = self.genes["fitness"](o, self.r)
            if fit > self.genelist[i][0]:
                old = self.genelist[i]
                self.genelist[i] = (fit, o)
                self.__checkReplaceExperimental(old)
                self.time_since_jump[i] = 0
            else:
                self.time_since_jump[i] += 1
                
        for i in xrange(len(self.experimental_genelist)):
            if self.experimental_genelist[i][1] is not None:
                o = self.mutateNew(self.experimental_genelist[i][1])
                fit = self.genes["fitness"](o, self.r)
                if fit > self.experimental_genelist[i][0]:
                    rm = self.__checkReplaceMain((fit, o), self.experimental_time_since_jump[i])
                    if rm[0]:
                        print("REPLACE MAIN")
                        temp = self.genelist[rm[1]]
                        self.genelist[rm[1]] = (fit, o)
                        self.time_since_jump[rm[1]] = 0
                        self.experimental_genelist[i] = temp
                        self.experimental_time_since_jump[i] = 0
                    else:
                        self.experimental_genelist[i] = (fit, o)
                        self.experimental_time_since_jump[i] = 0
                else:
                    self.experimental_time_since_jump[i] += 1
        return
    
    def __checkReplaceExperimental(self, gene):
        lowest = min([(self.experimental_genelist[i][0], i) for i in xrange(len(self.experimental_genelist))])
        if gene[0] > lowest[0]:
            print("NEW EXPERIMENTAL")
            self.experimental_genelist[lowest[1]] = gene
            self.experimental_time_since_jump[lowest[1]] = 0
        return
    
    def __checkReplaceMain(self, gene, jumps):
        lower = [(self.genelist[i], i) for i in xrange(len(self.genelist)) if ((gene[0] > self.genelist[i][0]) and (jumps < self.time_since_jump[i]))]
        if len(lower) < 1:
            return (False, 0)
        lower.sort()
        return (True, lower[0][1])
    