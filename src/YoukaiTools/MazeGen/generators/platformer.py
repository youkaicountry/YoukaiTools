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

from .. import baseGenerator
from .. import datatypes
import math
import random

#this could be used for subregions of levels or other generators
class basicGround():
    def __init__(self, r=random.Random()):
        self.land = None #the map
        self.r = r
   
    def get(self, parameters):
        return self.land
   
    #length, height, startheight, difficulty(0-1), flatness(0-1), brokenness(0-1), walkarray, runarray, runlength
    #runlength = the spaces it takes to achieve a run
    #walkarray/runarray = array that tells the maximum height that could be achieved at that distance (len tells max jump dist)
    def make(self, length, height, startheight, difficulty=.34, flatness=.7, brokenness=.01, walkarray=(4,2,10), runarray=(4,2,1,1), runlength=2):
        self.land = datatypes.BlockMap(length, height, False)
        isRunning = False
        distSinceBreak = 0
        distToRun = math.ceil(float(runlength) * ((1.0-difficulty)+1.0)) #distance we are assuming it will take to run 
        x = 0
        lastheight = startheight
      
        #place initial block
        print(x, startheight)
        for wy in range(startheight, height):
            self.land.setSpace(x, wy, True)
        x += 1
      
        while(x < length):
            #set up all the variables
            y = lastheight
            maxlength = (length - 1) - x
            heightchange = (self.r.random() > flatness) #will there be a height change involved
            maxup = y
            maxdown = (height-1) - y
            isRunning = distSinceBreak >= distToRun
            #pit? 
            ispit = self.r.random() <= brokenness
         
            dist = 0
            #get pit distance
            if ispit:
                i = self.r.triangular(0, 1, difficulty)
                if isRunning:
                    dist = math.floor(i*len(runarray))
                else:
                    dist = math.floor(i*len(walkarray))
            if maxlength < dist:
                dist = maxlength
            
            #determine if going up or down
            goingup = True
            goingup = self.r.triangular(0, 1, float(y) / float(height)) > .5
         
            #determine altitudechange
            altchange = 0
            if heightchange:
                i = self.r.triangular(0, 1, (difficulty + flatness) / 2.0)
                if ispit: print("I: "+str(i))
                if isRunning:
                    altchange = math.floor(i*runarray[dist])
                else:
                    altchange = math.floor(i*walkarray[dist])
            if goingup:
                if altchange > maxup: altchange = maxup
            else:
                if altchange > maxdown: altchange = maxdown
            
            #do the operation
            x += dist
            if goingup:
                y -= altchange
            else:
                y += altchange
            
            for wy in range(y, height):
                self.land.setSpace(x, wy, True)
            
            if dist > 0: 
                distSinceBreak = 1
            else:
                if altchange > 0 and goingup:
                    distSinceBreak = 1
                else:
                    distSinceBreak += 1
            x += 1
            lastheight = y
        return
    