import math

def atan2angle(y, x):
    a = math.atan2(y, x)
    if a < 0:
        a += 6.28318531
    return a
    