class testmath:
    a = 0
    b = 0
    c = 0
    
    def __init__(self, c):
        self.c = c
        
    def fit(self):
        return 1/abs((self.a + 2*self.b) - self.c)