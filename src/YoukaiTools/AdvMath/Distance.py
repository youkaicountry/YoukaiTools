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

import math

def manhattan2D(p1, p2):
    return abs(p2[0]-p1[0]) + abs(p2[1]-p1[1])
    
def euclidean2D(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
    
def euclideanEstimate2D(p1, p2):
    return (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2
    
def manhattan3D(p1, p2):
    return abs(p2[0]-p1[0]) + abs(p2[1]-p1[1]) + abs(p2[2]-p1[2])
    
def euclidean3D(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)
    
def euclideanEstimate3D(p1, p2):
    return (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2
    
def manhattanND(p1, p2, n=2):
    val = 0
    for i in range(n):
        val += abs(p2[i]-p1[i])
    return val
    
def euclideanND(p1, p2, n=2):
    val = 0
    for i in range(n):
        val += (p2[i]-p1[i])**2
    return math.sqrt(val)

def euclideanEstimateND(p1, p2, n=2):
    val = 0
    for i in range(n):
        val += (p2[i]-p1[i])**2
    return val
    