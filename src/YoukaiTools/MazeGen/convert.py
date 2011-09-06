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

from . import datatypes
import YoukaiTools.AdvMath.Numbers
from YoukaiTools import LineLoader

#intype should be a string or None to have it automatic.
#optimal will discard info in converting from block to maze, to
#make it the optimal maze for the given block map.
#blocked is the value used for the filler walls when going from maze to block
#outtype should also be a string. The types are:
#file - given as a filename
#array - given as a 2d nested list
#blockmap - given as a BlockMap object
#mazemap - given as a MazeMap object
def convertTo(inobj, outtype, intype=None, optimal=True, blocked=-1):
    if intype == None: it=getType(inobj)
    else: it=intype
    l = types2funcs[(it, outtype, optimal)]
    out = inobj
    for x in l:
        if x == mazeMap2BlockMap: out = x(out, blocked)
        else: out = x(out)
    return out
    
def saveFrom(filename, inobj, blocked=-1):
    t = getType(inobj)
    oo = convertTo(inobj, "array", blocked=blocked)
    saveArray(filename, oo)
    return

def loadAs(filename, outtype=None, optimal=True):
    oo = loadArray(filename)
    return convertTo(oo, outtype, optimal=optimal)

def getType(obj):
    return type2name[type(obj)]

def loadArray(filename):
    l = LineLoader.loadLinesFilename(filename, comments=[])
    return lines2Array(l)
    
def saveArray(filename, array):
    lines = array2Lines(array)
    f = open(filename, "w")
    l = [x.strip() + "\n" for x in lines]
    f.writelines(l)
    f.close()
    return

#file format is integers separated by spaces. Any non int
#and non space character(s) will be taken as none
def lines2Array(l):
    array = [item.split() for item in l]
    for y in range(len(array)):
        for x in range(len(array[y])):
            try:
                array[y][x] = int(array[y][x])
            except:
                array[y][x] = None
    return array

def array2Lines(array):
    out = []
    for y in range(len(array)):
        s = ""
        for x in range(len(array[0])):
            v = array[y][x]
            if v == None: v = "x"
            s = s + str(v) + " "
        out.append(s)
    return out
    
#takes an array[y][x]
def array2BlockMap(array):
    height = len(array)
    width = len(array[0])
    bm = datatypes.BlockMap(width, height)
    for y in range(height):
        for x in range(width):
            bm.setSpace(x, y, array[y][x])
    return bm
    

def blockMap2Array(blockmap):
    size = blockmap.getSize()
    arr = []
    for y in range(size[1]):
        arr.append([])
        for x in range(size[0]):
            arr[y].append(blockmap.getSpace(x, y))
    return arr

def blockMap2MazeMap(blockmap):
    s = blockmap.getSize()
    mm = datatypes.MazeMap(s[0], s[1])
    for y in range(s[1]):
        for x in range(s[0]):
            spaceval = blockmap.getSpace(x, y)
            if spaceval != None:
                #up
                v = spaceval
                if mm.getWall(x, y, datatypes.DIR_NORTH) != None: v = None
                mm.setWall(x, y, datatypes.DIR_NORTH, v)
                #down
                v = spaceval
                if mm.getWall(x, y, datatypes.DIR_SOUTH) != None: v = None
                mm.setWall(x, y, datatypes.DIR_SOUTH, v)
                #right
                v = spaceval
                if mm.getWall(x, y, datatypes.DIR_EAST) != None: v = None
                mm.setWall(x, y, datatypes.DIR_EAST, v)
                #left
                v = spaceval
                if mm.getWall(x, y, datatypes.DIR_WEST) != None: v = None
                mm.setWall(x, y, datatypes.DIR_WEST, v)
    return mm
    
def blockMap2MazeMapOptimal(blockmap):
    size = blockmap.getSize()
    #make the proper width and height
    w = int(size[0]/2) if not YoukaiTools.AdvMath.Numbers.isEven(size[0]) else int(size[0]/2 - 1)
    h = int(size[1]/2) if not YoukaiTools.AdvMath.Numbers.isEven(size[1]) else int(size[1]/2 - 1)
    m = datatypes.MazeMap(w, h)
    for y in range(h):
        yloc = y*2 + 1
        for x in range(w):
            xloc = x*2 + 1
            #up
            m.setWall(x, y, datatypes.DIR_NORTH, blockmap.getSpace(xloc, yloc-1))
            #down
            m.setWall(x, y, datatypes.DIR_SOUTH, blockmap.getSpace(xloc, yloc+1))
            #left
            m.setWall(x, y, datatypes.DIR_WEST, blockmap.getSpace(xloc-1, yloc))
            #right
            m.setWall(x, y, datatypes.DIR_EAST, blockmap.getSpace(xloc+1, yloc))
    return m

#make this use None as unblocked, anything else as blocked
def mazeMap2BlockMap(mazemap, blocked=True):
   msize = mazemap.getSize()
   #construct the block map
   blockmap = datatypes.BlockMap(msize[0]*2 + 1, msize[1]*2 + 1, None)
   bsize = blockmap.getSize()
   
   #construct the dots
   for y in range(0, bsize[1], 2):
      for x in range(0, bsize[0], 2):
         blockmap.setSpace(x, y, blocked)
         
   #fill the top
   for x in range(msize[0]):
      blockmap.setSpace(x*2 + 1, 0, mazemap.getWall(x, 0, datatypes.DIR_NORTH))
         
   #fill the left
   for y in range(msize[1]):
      blockmap.setSpace(0, y*2 + 1, mazemap.getWall(0, y, datatypes.DIR_WEST))
      
   #fill in the East Walls
   for y in range(msize[1]):
      for x in range(msize[0]):
         blockmap.setSpace(x*2 + 2, y*2 + 1, mazemap.getWall(x, y, datatypes.DIR_EAST))
   
   #fill in the East Walls
   for y in range(msize[1]):
      for x in range(msize[0]):
         blockmap.setSpace(x*2 + 1, y*2 + 2, mazemap.getWall(x, y, datatypes.DIR_SOUTH))
         
   return blockmap
   
type2name = {}
type2name[list] = "array"
type2name[datatypes.BlockMap] = "blockmap"
type2name[datatypes.MazeMap] = "mazemap"

types2funcs = {}
types2funcs[("array", "blockmap", False)] = [array2BlockMap]
types2funcs[("array", "mazemap", False)] = [array2BlockMap, blockMap2MazeMap]
types2funcs[("array", "array", False)] = []
types2funcs[("blockmap", "array", False)] = [blockMap2Array]
types2funcs[("blockmap", "mazemap", False)] = [blockMap2MazeMap]
types2funcs[("blockmap", "blockmap", False)] = []
types2funcs[("mazemap", "array", False)] = [mazeMap2BlockMap, blockMap2Array]
types2funcs[("mazemap", "blockmap", False)] = [mazeMap2BlockMap]
types2funcs[("mazemap", "mazemap", False)] = []

types2funcs[("array", "blockmap", True)] = [array2BlockMap]
types2funcs[("array", "mazemap", True)] = [array2BlockMap, blockMap2MazeMapOptimal]
types2funcs[("array", "array", True)] = []
types2funcs[("blockmap", "array", True)] = [blockMap2Array]
types2funcs[("blockmap", "mazemap", True)] = [blockMap2MazeMapOptimal]
types2funcs[("blockmap", "blockmap", True)] = []
types2funcs[("mazemap", "array", True)] = [mazeMap2BlockMap, blockMap2Array]
types2funcs[("mazemap", "blockmap", True)] = [mazeMap2BlockMap]
types2funcs[("mazemap", "mazemap", True)] = []

