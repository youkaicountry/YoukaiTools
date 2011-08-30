class TerrainFeature2D:
    def __init__(self):
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
        
    #public TerrainFeature2D()
    #{
    #    this.setAge(0);
    #    this.setBoundsRequiresValue(false);
    #    this.setMulAdd(1, 0);
    #    this.useClamp(false, 0, 1.0);
    #    this.useCache(true);
    #    return;
    #}
    
    #public TerrainFeature2D(double age, boolean bounds_requires_value, double mul, double add, boolean use_clamp, double clamp_low, double clamp_high, boolean use_cache)
    #{
    #    this.setAge(age);
    #    this.setBoundsRequiresValue(bounds_requires_value);
    #    this.setMulAdd(mul, add);
    #    this.useClamp(use_clamp, clamp_low, clamp_high);
    #    this.useCache(use_cache);
    #    return;
    #}
    
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
    
#    public boolean isInBounds(double x, double y, double under_value)
#    {
#        double cval = Double.NaN;
#        if (this.bounds_requires_value)
#        {
#            if (this.use_cache && (this.cached_x == x) && (this.cached_y == y))
#            {
#                cval = this.cached_value;
#            }
#            else
#            {
#                cval = this.getValue(x, y, under_value);
#            }
#        }
#        
#        return this.generateInBounds(x, y, cval, under_value);
#    }
#    
#    public void useCache(boolean use_cache)
#    {
#        this.use_cache = use_cache;
#        return;
#    }
#    
#    public void setMulAdd(double mul, double add)
#    {
#        this.mul = mul;
#        this.add = add;
#        this.flushCache();
#        return;
#    }
#    
#    public void setMul(double mul)
#    {
#        this.mul = mul;
#        this.flushCache();
#        return;
#    }
#    
#    public void setAdd(double add)
#    {
#        this.add = add;
#        this.flushCache();
#        return;
#    }
#    
#    public void useClamp(boolean use_clamp, double clamp_low, double clamp_high)
#    {
#        this.use_clamp = use_clamp;
#        this.clamp_low = clamp_low;
#        this.clamp_high = clamp_high;
#        this.flushCache();
#        return;
#    }
#    
#    public abstract double generateValue(double x, double y, double under_value);
#    
#    public abstract boolean generateInBounds(double x, double y, double this_value, double under_value);
#    
#    public void setAge(double age)
#    {
#        this.age = age;
#    }
#    
#    public double getAge()
#    {
#        return this.age;
#    }