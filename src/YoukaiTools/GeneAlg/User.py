#the gene class        
class Gene:
    #should return the fitness of obj.
    #do not modify obj
    def getFitness(self, obj):
        return 1
    
    #should return a mate of obj1 and obj2
    #do not modify obj1 and obj2
    def mate(self, obj1, obj2):
        return 1
    
    #should return a mutation of obj, keeping the intensity in mind
    def mutate(self, intensity, obj):
        return 1
    
    def getRandom(self):
        return 1
    
    def getBasic(self):
        return 1
    
    def report(self, obj, fitness, generation, topgeneration):
        return 1

#the options class
class Options:
    selection = 0
    deletion = 0
    fill = 0
    mutationchance = 0
    mutationintensitymin = 0
    mutationintensitymax = 0
    def __init__(self, selection, deletion, fill, mc, mimin, mimax):
        self.selection = selection
        self.deletion = deletion
        self.fill = fill
        self.mutationchance = mc
        self.mutationintensitymin = mimin
        self.mutationintensitymax = mimax