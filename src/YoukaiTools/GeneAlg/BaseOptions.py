class BaseSelect:
    settings = 0;
    
    def __init__(self, settings):
        self.settings = settings
    
    #should return the actual object
    def getSelection(self, objectlist):
        return objectlist[0]
    
    def getSettingsInfo(self):
        return ["info",]
    
    
class BaseFill:
    settings = 0
    genes = 0
    
    def __init__(self, settings, genes):
        self.settings = settings
        self.genes = genes
        
    def getFills(self, number):
        return [self.genes.getBasic(),]
    
