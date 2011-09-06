import math

#bump
#could be used for temperature of a planet from pole to pole
#sqrt(.5*(1+sin(x-1.6)^5))
#if p is odd the function will dip down at the poles
#if p is even the function will rise up at the poles
#mul does a multiplication before the sqrt, and rises and lowers it
#w determines how wide the function is.
def bump(x, mul=.5, p=5, w=1):
    return math.sqrt(mul*pow(w+math.sin(x-1.6),p) )

def sigmoid(x):
    return 1 / (1 + math.exp(-x))
