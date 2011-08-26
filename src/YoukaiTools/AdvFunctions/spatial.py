def arrayIndex2To1(x, y, width, offset=0):
    return y*width + x + offset

def arrayndex1To2(i, width, offset=0):
    ni = ni + offset
    return (ni%width, int(ni/width))

def atan2angle(y, x):
    a = math.atan2(y, x)
    if a < 0:
        a += 6.28318531
    return a

