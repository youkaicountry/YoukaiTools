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

from . import Vector
import math

#remember that for some stupid reason matrices go (height, width)

################################################################################
# MAKE MATRIX
################################################################################
def makeMatrix2(fillval=0):
    return [[fillval]*2]*2
    
def makeMatrix3(fillval=0):
    return [[fillval]*3, [fillval]*3, [fillval]*3]
    
def makeMatrixN(size=(2, 2), fillval=0):   
    return [[fillval]*size[1]]*size[0]

################################################################################
# MAKE IDENTITY / (RESET ORIENTATION)
################################################################################
def makeIdentity2(fillval=0, oneval=1):
    out = [[fillval]*2, [fillval]*2]
    out[0][0] = oneval
    out[1][1] = oneval
    return out
    
def setIdentity2(result, fillval=0, oneval=1):
    result[0][0] = oneval
    result[1][1] = oneval
    result[0][1] = fillval
    result[1][0] = fillval
    return
    
def makeIdentity3(fillval=0, oneval=1):
    out = [[fillval]*3, [fillval]*3, [fillval]*3]
    out[0][0] = oneval
    out[1][1] = oneval
    out[2][2] = oneval
    return out

def setIdentity3(result, fillval=0, oneval=1):
    result[0][0] = oneval
    result[1][1] = oneval
    result[2][2] = oneval
    result[0][1] = fillval
    result[0][2] = fillval
    result[1][0] = fillval
    result[1][2] = fillval
    result[2][0] = fillval
    result[2][1] = fillval
    return
    
def makeIdentityN(n=2, fillval=0, oneval=1):
    out = [[fillval]*n]*n
    for i in range(n):
        out[i][i] = oneval
    return out
    
def setIdentityN(result, n=2, fillval=0, oneval=1):
    for i in range(n):
        for j in range(n):
            if i == j: result[i][j] = oneval
            else: result[i][j] = fillval
    return
    
################################################################################
# ROTATE ORIENTATION
################################################################################
def rotateOrientation2():
    return
    
def rotateOrientation3(result, mat, rotvec, rotangle, tolerance=.003):
    if abs(rotangle) < tolerance: return mat
    pointtemp = [0, 0, 0]
    cosnormal = [0, 0, 0]
    sinnormal = [0, 0, 0]
    axisnormal = [0, 0, 0]
    Vector.normalizeVector3(axisnormal, rotvec)
    for count in range(3):
        Vector.copyVector(pointtemp, mat[count])
        Vector.crossProduct(sinnormal, axisnormal, pointtemp)
        Vector.normalizeVector3(sinnormal, sinnormal)
        Vector.crossProduct(cosnormal, sinnormal, axisnormal)
        Vector.normalizeVector3(cosnormal, cosnormal)
        
        dotproductvalue = Vector.dotProduct3(axisnormal, pointtemp)
        pointtemp[0]-=axisnormal[0]*dotproductvalue
        pointtemp[1]-=axisnormal[1]*dotproductvalue
        pointtemp[2]-=axisnormal[2]*dotproductvalue
        vectorlengthvalue = Vector.vectorLength3(pointtemp)
        
        result[count][0] = axisnormal[0]*dotproductvalue+cosnormal[0]*math.cos(rotangle)*vectorlengthvalue+sinnormal[0]*math.sin(rotangle)*vectorlengthvalue
        result[count][1] = axisnormal[1]*dotproductvalue+cosnormal[1]*math.cos(rotangle)*vectorlengthvalue+sinnormal[1]*math.sin(rotangle)*vectorlengthvalue
        result[count][2] = axisnormal[2]*dotproductvalue+cosnormal[2]*math.cos(rotangle)*vectorlengthvalue+sinnormal[2]*math.sin(rotangle)*vectorlengthvalue
        
        Vector.normalizeVector3(result[count], result[count])
    return
