import random

#the Base GA class
class BaseGA:
    
    def __init__(self, genes, options, savehistoryperiod, maxhistorylength):
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
            if len(self.history) > maxhistorylength:
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