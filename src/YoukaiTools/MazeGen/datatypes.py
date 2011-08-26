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
    def __init__(self, width, height, initval=None):
        self.map = []
        for y in range(height):
            self.map.append([])
            for x in range(width):
                self.map[y].append(initval)
        self.width = width
        self.height = height
    
    def isInBounds(self, x, y):
        if x < 0: return False
        if x >= self.width: return False
        if y < 0: return False
        if y >= self.height: return False
        return True
    
    def getSize(self):
      return (self.width, self.height)
    
    def getSpace(self, x, y):
      return self.map[y][x]
    
    def setSpace(self, x, y, val):
      self.map[y][x] = val
    
