import BaseGA

class Community(BaseGA.BaseGA):
    
    def __init__(self, genes, options, communitysize, savehistoryperiod, maxhistorylength):
        BaseGA.BaseGA.__init__(self, genes, options, savehistoryperiod, maxhistorylength) #call super constructor
        self.communitysize = communitysize
        o = self.options.fill.getFills(communitysize)
        self.genelist = []
        for i in range(self.communitysize):
            self.genelist.append((self.genes.getFitness(o[i]), o[i]))
            
        self.genelist.sort()        
            
        
    def doGeneration(self, number, honkevery):
        topgeneration = self.generation + number
        for i in xrange(number):
            oldlist = self.genelist
            self.genelist = []
            for j in xrange(self.communitysize):
                s1 = self.getSelectionNew(oldlist)
                s2 = self.getSelectionNew(oldlist)
                o = self.mateNew(oldlist[s1][1], oldlist[s2][1])
                f = self.mutateNew(o)
                self.genelist.append((self.genes.getFitness(f), f))
        self.generation+=1
        if self.generation % honkevery == 0:
                a = self.getBest()
                self.genes.report(a[1], a[0], self.generation, topgeneration)
        self.saveHistory()
        
        self.genelist.sort()

class Pool(BaseGA.BaseGA):
    
    def __init__(self, genes, options, poolsize, savehistoryperiod, maxhistorylength):
        BaseGA.BaseGA.__init__(self, genes, options, savehistoryperiod, maxhistorylength)
        self.poolsize = poolsize        
        o = self.options.fill.getFills(1)
        self.genelist = [(self.genes.getFitness(o[0]), o[0])]
        
    def doGeneration(self, number, honkevery):
        topgeneration = self.generation + number
        for i in xrange(number):
            s1 = self.getSelectionInPlace()
            s2 = self.getSelectionInPlace()
            o = self.mateInPlace(s1, s2)
            f = self.mutateNew(o)
            if len(self.genelist) < self.poolsize:
                self.genelist.append((self.genes.getFitness(f), f))
            else:
                d = self.getDeletionInPlace()
                self.genelist[d] = (self.genes.getFitness(f), f)
            self.generation+=1
            if self.generation % honkevery == 0:
                a = self.getBest()
                self.genes.report(a[1], a[0], self.generation, topgeneration)
            self.saveHistory()
            
        self.genelist.sort()

class HillClimb(BaseGA.BaseGA):
    def __init__(self, genes, options, savehistoryperiod, maxhistorylength):
        BaseGA.BaseGA.__init__(self, genes, options, savehistoryperiod, maxhistorylength)
        o = self.options.fill.getFills(1)
        self.genelist = [(self.genes.getFitness(o[0]), o[0])]
        
    def doGeneration(self, number, honkevery):
        topgeneration = self.generation + number
        for i in xrange(number):
            o = self.mutateInPlace(0)
            fit = self.genes.getFitness(o)
            if fit >= self.genelist[0][0]:
                self.genelist[0] = (fit, o)
            self.generation += 1
            if self.generation % honkevery == 0:
                a = self.getBest()
                self.genes.report(a[1], a[0], self.generation, topgeneration)
            self.saveHistory()
        self.genelist.sort()