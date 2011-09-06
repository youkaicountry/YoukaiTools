def arrayIndex2To1(x, y, width, offset=0):
    return y*width + x + offset

def arrayndex1To2(i, width, offset=0):
    ni = i + offset
    return (ni%width, int(ni/width))
