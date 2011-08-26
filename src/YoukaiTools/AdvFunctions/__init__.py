import math
from . import distance
from . import spatial

def sigmoid(x):
    return 1 / (1 + math.exp(-x))
    
def realatan2(y, x):
    v = math.atan2(y, x)
    if v < 0:
        return (math.pi-abs(v)) + math.pi
    return v

#bump
#could be used for temperature of a planet from pole to pole
#sqrt(.5*(1+sin(x-1.6)^5))
#if p is odd the function will dip down at the poles
#if p is even the function will rise up at the poles
#mul does a multiplication before the sqrt, and rises and lowers it
#w determines how wide the function is.
def bump(x, mul=.5, p=5, w=1):
    return math.sqrt(mul*pow(w+sin(x-1.6),p) )
    
#returns True if given number is even, False if odd
def isEven(x):
    return int(x) % 2 == 0

