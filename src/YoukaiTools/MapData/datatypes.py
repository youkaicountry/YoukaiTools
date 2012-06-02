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

from YoukaiTools import GraphEngine
from YoukaiTools.GraphEngine.GraphTools.SpecialTypes import GridGraph

DIR_NORTH = 0
DIR_SOUTH = 1
DIR_WEST = 2
DIR_EAST = 3

class MazeMap:
    def __init__(self, width, height, initval=None):
        self.width = width
        self.height = height
        self.walls = []
        for y in range(height+1):
            self.walls.append([])
            for x in range(width+1):
                self.walls[y].append([])
                self.walls[y][x].append(initval)
                self.walls[y][x].append(initval)
    
    def isInBounds(self, x, y):
        if x < -1: return False
        if x > self.width: return False
        if y < -1: return False
        if y > self.height: return False
        if x == -1 and y == -1: return False
        if x == -1 and y == self.height: return False
        if x == self.width and y == -1: return False
        if x == self.width and y == self.height: return False
        return True
        
    def isGoodDirection(self, x, y, dir):
        if dir == DIR_NORTH:
            if x >= self.width: return False
            if x < 0: return False
            if y > self.height: return False
            if y < 0: return False
        elif dir == DIR_SOUTH:
            if x >= self.width: return False
            if x < 0: return False
            if y >= self.height: return False
            if y < -1: return False
        elif dir == DIR_WEST:
            if y >= self.height: return False
            if y < 0: return False
            if x > self.width: return False
            if x < 0: return False
        elif dir == DIR_EAST:
            if y >= self.height: return False
            if y < 0: return False
            if x >= self.width: return False
            if x < -1: return False
        if x == -1 and y == -1: return False
        if x == -1 and y == self.height: return False
        if x == self.width and y == -1: return False
        if x == self.width and y == self.height: return False
        return True
        
    def getSize(self):
        return (self.width, self.height)
        
    def __getEffectiveSpace(self, x, y, direction):
        if direction == DIR_NORTH:
            return (x, y, 0)
        if direction == DIR_WEST:
            return (x, y, 1)
        if direction == DIR_SOUTH:
            return (x, y+1, 0)
            #return (x, (y+1) % (self.height), 0) #wrapping
        if direction == DIR_EAST:
            return (x+1, y, 1)
            #return ((x+1) % (self.width), y, 1) #wrapping
        return None
    
    def getWall(self, x, y, dir):
        space = self.__getEffectiveSpace(x, y, dir)
        return self.walls[int(space[1])][int(space[0])][int(space[2])]
    
    def setWall(self, x, y, dir, val):
        space = self.__getEffectiveSpace(x, y, dir)
        self.walls[space[1]][space[0]][space[2]] = val
        
    def getAllNeighbors(self, x, y):
        out = []
        if y > 0: out.append((x, y-1))
        if y < self.height-1: out.append((x, y+1))
        if x > 0: out.append((x-1, y))
        if x < self.width-1: out.append((x+1, y))
        return out
        
    def getAllNeighborsFull(self, x, y):
        out = 4*[None]
        if y > 0: out[0] = (x, y-1)
        if x < self.width-1: out[1] = (x+1, y)
        if y < self.height-1: out[2] = (x, y+1)
        if x > 0: out[3] = (x-1, y)
        return out
   
    def getAllNeighborDirections(self, x, y):
        out = []
        if y > 0: out.append(DIR_NORTH)
        if y < self.height-1: out.append(DIR_SOUTH)
        if x > 0: out.append(DIR_WEST)
        if x < self.width-1: out.append(DIR_EAST)
        return out
    
    def getAllUnblockedNeighbors(self, x, y, blocked):
        return [v for v in self.getAllNeighbors(x, y) if self.getWall(x, y, self.getDirection(x, y, v[0], v[1])) != blocked]
   
    def getDirection(self, fromx, fromy, tox, toy):
        if tox > fromx: return DIR_EAST
        if toy > fromy: return DIR_SOUTH
        if toy < fromy: return DIR_NORTH
        if tox < fromx: return DIR_WEST
        return None
    
class BlockMap:
    """
    A 2d tile based map data structure, with some useful utility functions.
    """
    def __init__(self, width, height, initval=None):
        """
        @param width: The width of the map.
        @param height: The height of the map.
        @param initval: The initial value of the spaces of the map. Defaults to None.
        """
        self.map = []
        for i in xrange(width*height):
            self.map.append(initval)
        self.width = width
        self.height = height
    
    def isInBounds(self, x, y):
        """
        Checks if the given coordinates are in the bounds of the map.
        @param x: The x coordinate to check.
        @param y: The y coordinate to check.
        @return: Whether the coordinates are in bounds.
        @rtype: C{bool}
        """
        if x < 0: return False
        if x >= self.width: return False
        if y < 0: return False
        if y >= self.height: return False
        return True
    
    def getSize(self):
        """
        Returns a tuple with the size of the map.
        @return: A tuple containing the size of the map.
        @rtype: C{iterable}
        """
        return (self.width, self.height)
    
    def getSpace(self, x, y):
        """
        Gets the value of the space at the given coordinates.
        @param x: The x coordinate.
        @param y: The y coordinate.
        @return: The value of the space.
        """
        return self.map[y*self.width+x]
    
    def setSpace(self, x, y, val):
        """
        Sets the value of the space at the given coordinates.
        @param x: The x coordinate.
        @param y: The y coordinate.
        @param val: The value to set for the space.
        """
        self.map[y*self.width+x] = val
    
    # spaces should be a list of tuples (x, y, val),
    # if they are only (x, y), then default_val will be used
    def setSpaces(self, spaces, default_val=True):
        """
        Sets a list of spaces.
        @param spaces: A list to spaces to set. The value for each space should be either a 2 long tuple with (x, y), in which case the default_val is used, or it should be (x, y, val).
        @type spaces: C{iterable}
        @default_val: The default value to set if only coordinates are given for a space.
        """
        for space in spaces:
            x = space[0]
            y = space[1]
            if len(space) == 3:
                val = space[2]
            else:
                val = default_val
            self.map[y*self.width+x] = val
        return

class BlockMapPathing(BlockMap):
    """
    An instance of BlockMap that has a pathfinding graph built in.
    """
    def __init__(self, width, height, initval=None, blocked_condition=lambda x: x is True, diagonals=False, wrap=False):
        BlockMap.__init__(self, width, height, initval)
        self.graph = GraphEngine.Graphs.BasicGraph()
        self.blocked_condition = blocked_condition
        self.diagonals = diagonals
        self.wrap = wrap
        self.__constructMap()
        return
    
    def setSpace(self, x, y, val):
        BlockMap.setSpace(self, x, y, val)
        self.__constructSpace(x, y)
        return
    
    def setSpaces(self, spaces, default_val=True):
        BlockMap.setSpaces(self, spaces, default_val)
        for space in spaces:
            self.__constructSpace(space[0], space[1])
        return
    
    def __constructMap(self):
        for y in xrange(self.height):
            for x in xrange(self.width):
                self.__constructSpace(x, y)
        return
    
    def __constructSpace(self, x, y):
        #we need tp remove else.
        if not self.blocked_condition(self.getSpace(x, y)):
            GridGraph.addVertexToGridGraph(self.graph, (x, y))
        else:
            GridGraph.removeVertexFromGraph(self.graph, (x, y))
        return
    