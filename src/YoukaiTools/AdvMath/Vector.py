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

from math import sqrt

#TODO: make it all in place

################################################################################
# DOT PRODUCT
################################################################################
def dotProduct2(vec1, vec2):
    return vec1[0]*vec2[0] + vec1[1]*vec2[1]

def dotProduct3(vec1, vec2):
    return vec1[0]*vec2[0] + vec1[1]*vec2[1] + vec1[2]*vec2[2]

def dotProductN(vec1, vec2, n=None):
    if n is None: n = len(vec1)
    out = 0
    for i in range(n):
        out += vec1[i]*vec2[i]
    return out

################################################################################
# CROSS PRODUCT
################################################################################
def crossProduct(result, vec1, vec2):
    result[0] = vec2[1]*vec1[2] - vec2[2]*vec1[1]
    result[1] = vec2[2]*vec1[0] - vec2[0]*vec1[2]
    result[2] = vec2[0]*vec1[1] - vec2[1]*vec1[0]
    return

################################################################################
# LENGTH
################################################################################
def vectorLength2(vec):
    return sqrt(vec[0]**2 + vec[1]**2)
    
def vectorLength3(vec):
    return sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
    
def vectorLengthN(vec, n=None):
    if n is None: n = len(vec)
    add = 0
    for i in range(n):
        add += vec[i]**2
    return sqrt(add)

################################################################################
# NORMALIZE
################################################################################
def normalizeVector2(result, vec):
    vlength = vectorLength2(vec)
    if vlength != 0:
        vlength = 1.0/vlength
        result[0] = vec[0]*vlength
        result[1] = vec[1]*vlength
    return result

def normalizeVector3(result, vec):
    vlength = vectorLength3(vec)
    if vlength != 0:
        vlength = 1.0/vlength
        result[0] = vec[0]*vlength
        result[1] = vec[1]*vlength
        result[2] = vec[2]*vlength
    return result

def normalizeVectorN(result, vec, n=None):
    if n is None: n = len(vec)
    vlength = vectorLengthN(vec, n)
    if vlength != 0:
        vlength = 1.0/vlength
        for i in range(n):
            result[i] = vec[i]/vlength
    return result

################################################################################
# COPY
################################################################################
def copyVector(result, vec):
    for i in range(len(vec)):
        result[i] = vec[i]
    return

################################################################################
# ADD
################################################################################
def addVectors2(result, vec1, vec2):
    result[0] = vec1[0] + vec2[0]
    result[1] = vec1[1] + vec2[1]
    return
    
def addVectors3(result, vec1, vec2):
    result[0] = vec1[0] + vec2[0]
    result[1] = vec1[1] + vec2[1]
    result[2] = vec1[2] + vec2[2]
    return
    
def addVectorsN(result, vec1, vec2, n=None):
    if n is None: n = len(vec1)
    for i in range(n):
        result[i] = vec1[i] + vec2[i]
    return
    
################################################################################
# SUBTRACT
################################################################################
def subtractVectors2(result, vec1, vec2):
    result[0] = vec1[0] - vec2[0]
    result[1] = vec1[1] - vec2[1]
    return
    
def subtractVectors3(result, vec1, vec2):
    result[0] = vec1[0] - vec2[0]
    result[1] = vec1[1] - vec2[1]
    result[2] = vec1[2] - vec2[2]
    return
    
def subtractVectorsN(result, vec1, vec2, n=None):
    if n is None: n = len(vec1)
    for i in range(n):
        result[i] = vec1[i] - vec2[i]
    return

################################################################################
# SCALE
################################################################################
def scaleVector2(result, vec1, scale):
    result[0] = vec1[0] * scale
    result[1] = vec1[1] * scale
    return
    
def scaleVector3(result, vec1, scale):
    result[0] = vec1[0] * scale
    result[1] = vec1[1] * scale
    result[2] = vec1[2] * scale
    return
    
def scaleVectorN(result, vec, scale, n=None):
    if n is None: n = len(vec)
    for i in range(n):
        result[i] = vec[i] * scale
    return
    
################################################################################
# SCALE ADD
################################################################################
def scaleAddVectors2(result, vec1, vec2, scale):
    result[0] = vec1[0] + vec2[0] * scale
    result[1] = vec1[1] + vec2[1] * scale
    return
    
def scaleAddVectors3(result, vec1, vec2, scale):
    result[0] = vec1[0] + vec2[0] * scale
    result[1] = vec1[1] + vec2[1] * scale
    result[2] = vec1[2] + vec2[2] * scale
    return
    
def scaleAddVectorsN(result, vec1, vec2, scale, n=None):
    if n is None: n = len(vec1)
    for i in range(n):
        result[i] = vec1[i] + vec2[i] * scale
    return

################################################################################
# MAKE VECTOR
################################################################################
def makeVector2(fillval=0):
    return [fillval, fillval]
    
def makeVector3(fillval=0):
    return [fillval, fillval, fillval]
    
def makeVectorN(n=2, fillval=0):
    return [fillval]*n
    