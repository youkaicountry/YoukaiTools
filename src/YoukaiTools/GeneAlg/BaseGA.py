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
import time

import Data

#the Base GA class
class BaseGA:
    def __init__(self, genes, options, savehistoryperiod=10000, maxhistorylength=10):
        self.genes = genes
        self.options = options
        self.genelist = []
        self.history = []
        self.generation = 0
        self.savehistoryperiod = savehistoryperiod
        self.maxhistorylength = maxhistorylength
        self.time = 0
        self.need_sort = True

    #make criteria checked variables relative to start condition
    def run(self, report_criteria, save_criteria, termination_criteria, batch_size=1):
        crit_objs = [self.__make_crit(), self.__make_crit(), self.__make_crit()]
        while True:
            t0 = time.clock()
            for i in range(batch_size):
                self.doGeneration()
                if self.need_sort: self.genelist.sort()
            tdelta = time.clock() - t0
            gdelta = batch_size
            self.generation += gdelta
            self.time += tdelta
            for c in crit_objs:
                c["generations"] += gdelta
                c["time"] += tdelta
            a = self.getBest()
            r = Data.make_report(a[1], a[0], self.generation, termination_criteria["generations"], self.time, termination_criteria["time"])
            if self.checkCriteria(report_criteria, crit_objs[0]): self.genes["report"](r)
            if self.checkCriteria(save_criteria, crit_objs[1]): self.saveHistory()
            if self.checkCriteria(termination_criteria, crit_objs[2]): break
        return
    
    def __make_crit(self):
        d = {}
        d["generations"] = 0
        d["time"] = 0
        return d
    
    def checkCriteria(self, criteria, cobj):
        t = False
        for k in criteria.keys():
            if criteria[k] is not None:
                if cobj[k] >= criteria[k]:
                    t = True
                    cobj[k] = 0
        return t
    
    #a list of tuples [(fitness, dna), ...]
    def getGeneList(self):
        return self.genelist
    
    #returns the index of the selected object
    def getSelectionInPlace(self):
        return self.options["selection"](self.genelist, *self.options["selection_settings"])
    
    def getSelectionNew(self, objectlist):
        return self.options["selection"](objectlist, *self.options["selection_settings"])
    
    #returns the index of the object to be deleted
    def getDeletionInPlace(self):
        return self.options["deletion"](self.genelist, *self.options["deletion_settings"])
    
    def getDeletionNew(self, objectlist):
        return self.options["deletion"](objectlist, *self.options["deletion_settings"])
    
    #returns the mutated object genelist object (fitness, obj)
    def mutateGeneListObject(self, index):
        r = random.random()
        if r <= self.options["mutation_chance"]:
            c = random.random()
            c *= self.options["mutation_intensity_max"]-self.options["mutation_intensity_min"]
            c += self.options["mutation_intensity_min"]
            o = self.genes["mutate"](c, self.genelist[index][1])
            return o
        return self.genelist[index][1]
    
    #returns the mutated object genelist object (fitness, obj)
    def mutateNew(self, obj):
        r = random.random()
        if r <= self.options["mutation_chance"]:
            #print "chance"
            c = random.random()
            c *= self.options["mutation_intensity_max"]-self.options["mutation_intensity_min"]
            c += self.options["mutation_intensity_min"]
            o = self.genes["mutate"](c, obj)
            return o
        return obj
    
    def saveHistory(self):
        a = self.getBest()
        self.history.append((self.generation, a[0], a[1]))
        if len(self.history) > self.maxhistorylength:
            a = len(self.history)-self.maxhistorylength
            self.history = self.history[a:]
        return
    
    #returns the mated object(object only)
    def mateInPlace(self, index1, index2):
        return self.genes["mate"](self.genelist[index1][1], self.genelist[index2][1])
    
    def mateNew(self, obj1, obj2):
        return self.genes["mate"](obj1, obj2)    
    
    #does a single generation
    def doGeneration(self, number, honkevery):
        return 1
    
    def getBest(self):
        return self.genelist[len(self.genelist)-1]
    
    def getHistory(self):
        return self.history
    
    def clearHistory(self):
        self.history = []
        
