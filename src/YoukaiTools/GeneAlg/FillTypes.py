import BaseOptions

class BasicFill(BaseOptions.BaseFill):
    
    def __init__(self, genes):
        BaseOptions.BaseFill.__init__(self, 0, genes)
        
    def getFills(self, number):
        r = []
        for i in range(number):
            r.append(self.genes.getBasic())
        return r