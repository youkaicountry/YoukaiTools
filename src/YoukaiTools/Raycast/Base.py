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
    