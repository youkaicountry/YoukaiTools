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

from .. import datatypes
import random
from .. import convert

#a recursive backtracker maze
#takes the actual maze size, the out put is that size*2 + 1
class recursiveBacktrackMaze():
   def __init__(self, r=random.Random()):
      self.maze = None
      self.found = None
      self.path = None
      self.converted = None
      self.blocked = None
      self.r = r
      self.nx = 0
      self.ny = 0
      
   #param = "blockmap" -> returns a blockmap
   #param = "mazemap" -> return a mazemap
   def get(self, outputtype):
       if outputtype == "blockmap":
           if self.converted != None: return self.converted
           self.converted = convert.mazeMap2BlockMap(self.maze, self.blocked)
           return self.converted
       elif outputtype == "mazemap":
           return self.maze
       return None
   
   def __recursiveBacktrack(self, x, y, blocked, unblocked=None):
      nx = x
      ny = y
      self.path.append((x, y))
      while len(self.path) > 0:
         self.found.setSpace(nx, ny, blocked)
         n = self.maze.getAllNeighbors(nx, ny)
         #print "OUT: "+str(n)
         realn = []
         for o in n:
            if self.found.getSpace(o[0], o[1]) is None:
               realn.append(o)
         if len(realn) > 0:
            self.path.append((nx, ny))
            #self.r.shuffle(realn)
            choice = self.r.randint(0, len(realn)-1)
            if self.found.getSpace(realn[choice][0], realn[choice][1]) is None:
               dir = self.maze.getDirection(nx, ny, realn[choice][0], realn[choice][1])
               self.maze.setWall(nx, ny, dir, None)
               nx = realn[choice][0]
               ny = realn[choice][1]
               continue
         else:
            if len(self.path) == 0: break
            else:
               a = self.path.pop(len(self.path)-1)
               nx = a[0]
               ny = a[1]
               continue
      return
      
   #parameters contains (width, height, startx, starty, blocked)
   def make(self, width, height, startx=0, starty=0, blocked=0, unblocked=None):
      self.path = []
      self.blocked = blocked
      self.found = datatypes.BlockMap(width, height, unblocked)
      self.maze = datatypes.MazeMap(width, height, blocked)
      self.found = datatypes.BlockMap(width, height, unblocked)
      self.__recursiveBacktrack(startx, starty, blocked)
      return
