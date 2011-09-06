import math

#def atan2angle(y, x):
#    a = math.atan2(y, x)
#    if a < 0:
#        a += 6.28318531
#    return a

def atan2_angle(y, x):
    v = math.atan2(y, x)
    if v < 0:
        return (math.pi-abs(v)) + math.pi
    return v
