import random
import itertools

class AdvRandom:
    def __init__(self, r=None):
        if r == None:
            self.r = random.Random()
        else:
            self.r = r
        return
        
    def biasedChoice(self, seq, probseq=None):
        #Chooses an element from seq at random
        #Probability of each element given in probseq
        if probseq == None:
            probseq = itertools.repeat(1.0)
        total = sum(p for e,p in zip(seq, probseq))
        r = random.uniform(0.0, total)
        for e,p in zip(seq, self.__partialsum(probseq)):
            if p >= r:
                return e
        raise RuntimeError("Could not find element (total="+str(total)+", r="+str(r))
        
    def __partialsum(self, seq):
        total = 0.0
        for x in seq:
            total += x
            yield total
        return
        
_inst = AdvRandom()
biasedChoice = _inst.biasedChoice

