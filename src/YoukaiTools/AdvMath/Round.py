import math

def roundDown(n):
    return math.floor(n)
    
def roundUp(n):
    return math.ceil(n)
    
def roundEven(n):
    return round(n)
    
def roundLow(n):
    return int(n)
    
def roundHigh(n):
    return math.floor(n) if n < 0 else math.ceil(n)
