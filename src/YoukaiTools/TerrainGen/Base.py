class TerrainFeature2D:
    def __init__(self):
        self.age = 0                          #A general number that represents the order in which to apply modifiers
    
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