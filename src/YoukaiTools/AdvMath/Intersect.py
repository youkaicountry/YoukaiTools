#Copyright (c) <2011> <Nathaniel Caldwell>

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

#from . import Vector

#rect should be (left, top, right, bottom)
#if calcirect, return will be (intersect?, irect)
#else return will be intersect?
def rectxRect(rect1, rect2, calcirect=True):
    intersect = not((rect2[0]>rect1[2])or(rect2[2]<rect1[0])or(rect2[1]>rect1[3])or(rect2[3]<rect1[1]))
    if not calcirect: return intersect
    if not intersect:
        irect=(0, 0, 0, 0)
    else:
        irect=(max(rect1[0], rect2[0]), max(rect1[1], rect2[1]), min(rect1[2], rect2[2]), min(rect1[3], rect2[3]))
    return (intersect, irect)

#UNFINISHED
#intersectpoint = result, vector3
#normal = the plane's normal
#scale = float of ?
#startpoint = vector3 line start?
#endpoint = vector3 line end?
#point = vector3 plane?
#def lineXPlane(intersectpoint, normal, startpoint, endpoint, point):
#    vec = [0, 0, 0]
#    vec2 = [0, 0, 0]
#    Vector.subtractVectors3(vec, endpoint, point)
#    if Vector.dotProduct3(vec, normal) > 0: return False
#    
#    return
