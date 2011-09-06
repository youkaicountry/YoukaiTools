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
        
    #returns the index of the selected object
    def getSelectionInPlace(self):
        return self.options.selection.getSelection(self.genelist)
    
    def getSelectionNew(self, objectlist):
        return self.options.selection.getSelection(objectlist)
    
    #returns the index of the object to be deleted
    def getDeletionInPlace(self):
        return self.options.deletion.getSelection(self.genelist)
    
    def getDeletionNew(self, objectlist):
        return self.options.deletion.getSelection(objectlist)
    
    #returns the mutated object genelist object (fitness, obj)
    def mutateInPlace(self, index):
        r = random.random()
        if r <= self.options.mutationchance:
            c = random.random()
            c *= self.options.mutationintensitymax-self.options.mutationintensitymin
            c += self.options.mutationintensitymin
            o = self.genes.mutate(c, self.genelist[index][1])
            return o
        return self.genelist[index][1]
    
    #returns the mutated object genelist object (fitness, obj)
    def mutateNew(self, obj):
        r = random.random()
        if r <= self.options.mutationchance:
            #print "chance"
            c = random.random()
            c *= self.options.mutationintensitymax-self.options.mutationintensitymin
            c += self.options.mutationintensitymin
            o = self.genes.mutate(c, obj)
            return o
        return obj
    
    def saveHistory(self):
        if (self.generation % self.savehistoryperiod) == 0:
            self.genelist.sort()
            a = self.getBest()
            self.history.append((self.generation, a[0], a[1]))
            if len(self.history) > self.maxhistorylength:
                a = len(self.history)-self.maxhistorylength
                self.history = self.history[a:]
        return
    
    #returns the mated object(object only)
    def mateInPlace(self, index1, index2):
        return self.genes.mate(self.genelist[index1][1], self.genelist[index2][1])
    
    def mateNew(self, obj1, obj2):
        return self.genes.mate(obj1, obj2)    
    
    #does a single generation
    def doGeneration(self, number, honkevery):
        return 1
    
    def getBest(self):
        return self.genelist[len(self.genelist)-1]
    
    def getHistory(self):
        return self.history
    
    def clearHistory(self):
        self.history = []