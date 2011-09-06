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

class RayCaster:
    def __init__(self, screensize):
        self.position = [0, 0]
        self.direction = [-1, 0]
        self.worldmap =  None
        self.camplane = [0.0, .66]
        self.screensize = screensize
        return
        
    def setPosition(self, newposition):
        self.position[0] = newposition[0]
        self.position[1] = newposition[1]
    
    def getPosition(self):
        return self.position
    
    def move(self, dist):
        return
        #if self.worldmap.getValue(int(self.position[0] + self.direction[0] * dist),int(self.position[1])) == 0.0: self.position[0] += self.direction[0] * dist
        #if self.worldmap.getValue(int(self.position[0]),int(self.position[1] + self.direction[1] * dist)) == 0.0: self.position[1] += self.direction[1] * dist
   
    def turn(self, angle):
        olddirx = self.direction[0];
        self.direction[0] = self.direction[0] * math.cos(angle) - self.direction[1] * math.sin(angle)
        self.direction[1] = olddirx * math.sin(angle) + self.direction[1] * math.cos(angle)
        oldplanex = self.camplane[0]
        self.camplane[0] = self.camplane[0] * math.cos(angle) - self.camplane[1] * math.sin(angle)
        self.camplane[1] = oldplanex * math.sin(angle) + self.camplane[1] * math.cos(angle)
       
    def raycast(self, screen=None):
        return
    