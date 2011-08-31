class TerrainFeature2D:
    def __init__(self, age=0, bounds_requires_value=False, mul=1, add=0, use_clamp=False, clamp_low=0.0, clamp_high=1.0, use_cache=True):
        self.age = 0                          #A general number that represents the order in which to apply modifiers

        #Use the cache to speed up repeated hits on the same location. You should NOT use it if
        #there are random elements at play in determining the value.
        #TODO: Have a larger cache
        self.use_cache = False                #Use the cache?
        self.cached_x = None                  #cached location x
        self.cached_y = None                  #cached location y
        self.cached_value = None              #cached value
    
        self.use_clamp = False                #clamp the values?
        self.clamp_low = 0                    #clamp floor
        self.clamp_high = 1.0                 #clamp ceiling
    
        self.mul = 1                          #value multiplier
        self.add = 0                          #value add
    
        self.bounds_requires_value = False    #must be true if the bounds function requires the value

        self.setAge(age)
        self.setBoundsRequiresValue(bounds_requires_value)
        self.setMulAdd(mul, add)
        self.useClamp(use_clamp, clamp_low, clamp_high)
        self.useCache(use_cache)
        return
    
    def getValue(self, x, y, under_value):
        cval = 0
        
        #retrieve cached value, if available
        if self.use_cache and (self.cached_x == x) and (self.cached_y == y):
            return self.cached_value
        else:
            cval = self.generateValue(x, y, under_value)
        
        #apply mul and add
        cval = (cval*self.mul) + self.add
        
        #apply clamp
        if self.use_clamp:
            if cval < self.clamp_low:
                cval = self.clamp_low
            elif cval > self.clamp_high:
                cval = self.clamp_high
        
        #store cached value
        if self.use_cache:
            self.cached_x = x;
            self.cached_y = y;
            self.cached_value = cval;
        
        return cval
    
    def setBoundsRequiresValue(self, brv):
        self.bounds_requires_value = brv
        return
    
    def flushCache(self):
        self.cached_x = None
        self.cached_y = None
        self.cached_value = None
        return
    
    def isInBounds(self, x, y, under_value):
        cval = None
        if self.bounds_requires_value:
            if self.use_cache and (self.cached_x == x) and (self.cached_y == y):
                cval = self.cached_value
            else:
                cval = self.getValue(x, y, under_value)
        return self.generateInBounds(x, y, cval, under_value)
    
    def useCache(self, use_cache):
        self.use_cache = use_cache
        return
    
    def setMulAdd(self, mul, add):
        self.mul = mul
        self.add = add
        self.flushCache()
        return

    def setMul(self, mul):
        self.mul = mul
        self.flushCache()
        return
    
    def setAdd(self, add):
        self.add = add
        self.flushCache()
        return
    
    def useClamp(self, use_clamp, clamp_low, clamp_high):
        self.use_clamp = use_clamp
        self.clamp_low = clamp_low
        self.clamp_high = clamp_high
        self.flushCache()
        return

    #THIS MUST BE FILLED IN BY THE USER CLASS
    def generateValue(self, x, y, under_value):
        return

    #THIS MUST BE FILLED IN BY THE USER CLASS
    def generateInBounds(self, x, y, this_value, under_value):
        return
    
    def setAge(self, age):
        self.age = age
        return
    
    def getAge(self):
        return self.age
