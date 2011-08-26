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
    