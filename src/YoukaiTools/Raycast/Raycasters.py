import math
from . import Base
from YoukaiTools import PyRange
import YoukaiTools.AdvMath.Trig
from YoukaiTools import MazeGen

pi_o_2 = math.pi / 2

class RaycastMaze(Base.RayCaster):
    def __init__(self, mazemap, screensize, spritelist=None):
        Base.RayCaster.__init__(self, screensize)
        self.output = []
        self.collision = {}
        self.stepstate = "still"
        self.stepdt = 0
        self.stepposition = 0
        self.stepdir = 0
        #graph, interp, tension, bias
        self.moving_graph = [None, None, 0, 0]
        self.turning_graph = [None, None, 0, 0]
        self.blocked_graph = [None, None, 0, 0]
        
        for x in range(screensize[0]):
            self.output.append(None)
        self.mazemap = mazemap
        self.setOptions(True, False if spritelist==None else True, 0, 0)
        self.spritelist=spritelist
        return
    
    #
    def setOptions(self, drawwalls=None, drawsprites=None, maxwalldist=None, maxspritedist=None):
        if drawwalls != None:
            self.drawwalls = drawwalls
        if drawsprites != None:
            self.drawsprites = drawsprites
        if maxwalldist != None:
            self.maxwalldist = maxwalldist
        if maxspritedist != None:
            self.maxspritedist = maxspritedist
        return
        
    def setMovingGraph(self, graph, interp=PyRange.Interpolation.cosine, tension=0, bias=0):
        self.moving_graph = [graph, interp, tension, bias]
        return
        
    def setTurningGraph(self, graph, interp=PyRange.Interpolation.cosine, tension=0, bias=0):
        self.turning_graph = [graph, interp, tension, bias]
        return
        
    def setBlockedGraph(self, graph, interp=PyRange.Interpolation.cosine, tension=0, bias=0):
        self.blocked_graph = [graph, interp, tension, bias]
        return
    
    #call each frame to do any step moving
    def updateStep(self):
        if self.stepposition >= 1: self.stepstate = "still"
        if self.stepstate != "turning":
            #make sure the player is facing a cardinal direction
            at = YoukaiTools.AdvMath.Trig.atan2_angle(self.direction[1], self.direction[0])
            at2 = YoukaiTools.AdvMath.Trig.atan2_angle(math.floor(self.direction[1] + .5), math.floor(self.direction[0] + .5))
            self.turn(at2 - at)
            if self.stepstate != "moving" and self.stepstate != "blocked":
                self.position[0] = int(self.position[0])+.5
                self.position[1] = int(self.position[1])+.5
            else: #player is moving. check for blocked move
                if self.stepstate == "blocked":
                    currpo = self.blocked_graph[0].getValue(self.stepposition, self.blocked_graph[1], self.blocked_graph[2], self.blocked_graph[3])
                    self.stepposition += self.stepdt
                    if self.stepposition >= 1: self.stepposition = 1
                    nextpo = self.blocked_graph[0].getValue(self.stepposition, self.blocked_graph[1], self.blocked_graph[2], self.blocked_graph[3])
                    self.move(self.stepdir*(nextpo - currpo))
                else:
                    currpo = self.moving_graph[0].getValue(self.stepposition, self.moving_graph[1], self.moving_graph[2], self.moving_graph[3])
                    self.stepposition += self.stepdt
                    if self.stepposition >= 1: self.stepposition = 1
                    nextpo = self.moving_graph[0].getValue(self.stepposition, self.moving_graph[1], self.moving_graph[2], self.moving_graph[3])
                    self.move(self.stepdir*(nextpo - currpo))
        else: #player is turning
            currpo = self.turning_graph[0].getValue(self.stepposition, self.turning_graph[1], self.turning_graph[2], self.turning_graph[3])
            self.stepposition += self.stepdt
            if self.stepposition >= 1: self.stepposition = 1
            nextpo = self.turning_graph[0].getValue(self.stepposition, self.turning_graph[1], self.turning_graph[2], self.turning_graph[3])
            self.turn(pi_o_2*(self.stepdir*(nextpo - currpo)))
        return
    
    #call to start a move
    #direction should be -1 or 1
    def startMove(self, frames, direction):
        if self.stepstate != "still": return
        self.stepdir = direction
        self.stepposition = 0
        self.stepdt = 1.0 / float(frames)
        destx = math.floor(self.position[0] + self.direction[0] * direction)
        desty = math.floor(self.position[1] + self.direction[1] * direction)
        cx = math.floor(self.position[0])
        cy = math.floor(self.position[1])
        d = self.mazemap.getDirection(cx, cy, destx, desty)
        w = self.mazemap.getWall(cx, cy, d)
        if w != None:
            if self.collision[w]: self.stepstate = "blocked"
            else:
                self.stepstate = "moving"
        else:
            self.stepstate = "moving"
        
        return
    
    #call to start a turn
    def startTurn(self, frames, direction):
        if self.stepstate != "still": return
        self.stepdir = direction
        self.stepposition = 0
        self.stepdt = 1.0 / float(frames)
        self.stepstate = "turning"
        return
        
    def setCollision(self, idnum, collide):
        self.collision[idnum] = collide
        return
        
    def move(self, dist):
        #mxd = self.mazemap.getDirection(0, 0, stepx, 0)
        #mxy = self.mazemap.getDirection(0, 0, 0, stepy)
        destx = math.floor(self.position[0] + self.direction[0] * dist)
        desty = math.floor(self.position[1] + self.direction[1] * dist)
        cx = math.floor(self.position[0])
        cy = math.floor(self.position[1])
        xmove = True
        ymove = True
        #have a blocked ids list
        if cx != destx:
            d = self.mazemap.getDirection(cx, 0, destx, 0)
            w = self.mazemap.getWall(cx, cy, d)
            if w != None:
                if self.collision[w]: xmove = False
        if cy != desty:
            d = self.mazemap.getDirection(0, cy, 0, desty)
            w = self.mazemap.getWall(cx, cy, d)
            if w != None:
                if self.collision[w]: ymove = False
        if xmove: self.position[0] += self.direction[0] * dist
        if ymove: self.position[1] += self.direction[1] * dist
        
        #if self.mazemap.getWall(int(self.position[0] + self.direction[0] * dist),int(self.position[1]), m) == 0.0: self.position[0] += self.direction[0] * dist
        #if self.mazemap.getWall(int(self.position[0]),int(self.position[1] + self.direction[1] * dist)) == 0.0: self.position[1] += self.direction[1] * dist
        return
        
    def raycast(self, screen=None):
        if screen == None: op = self.output
        else: op = screen
        for x in range(self.screensize[0]):
            camerax = (2.0 * x / float(self.screensize[0])) - 1.0 #x-coordinate in camera space
            if camerax == 0: camerax = camerax + .0001
            rayposx = self.position[0]
            rayposy = self.position[1]
            raydirx = self.direction[0] + (self.camplane[0] * camerax)
            raydiry = self.direction[1] + (self.camplane[1] * camerax)
            
            #which box of the map we're in  
            mapx = int(rayposx)
            mapy = int(rayposy)
            
            #length of ray from current position to next x or y-side
            sidedistx = 0
            sidedisty = 0
            
            #location in texture to draw
            mu = 0 #0 - 1
            
            #length of ray from one x or y-side to next x or y-side
            deltadistx = math.sqrt(1 + (raydiry * raydiry) / (raydirx * raydirx))
            deltadisty = math.sqrt(1 + (raydirx * raydirx) / (raydiry * raydiry))
            perpwalldist = 0
           
            #what direction to step in x or y-direction (either +1 or -1)
            stepx = 0
            stepy = 0
            
            hit = 0 #was there a wall hit?
            side = 0 #was a NS or a EW wall hit? 0 = NS, 1 = EW
            
            #calculate setp and initial sidedist
            if raydirx < 0:
                stepx = -1
                sidedist = sidedistx = (rayposx - mapx) * deltadistx
            else:
                stepx = 1
                sidedistx = (mapx + 1.0 - rayposx) * deltadistx
            if raydiry < 0:
                stepy = -1
                sidedisty = (rayposy - mapy) * deltadisty
            else:
                stepy = 1
                sidedisty = (mapy + 1.0 - rayposy) * deltadisty
                
            mxd = self.mazemap.getDirection(0, 0, -stepx, 0)
            myd = self.mazemap.getDirection(0, 0, 0, -stepy)
            
            mapval = 0
            
            #perform DDA
            while hit == 0:
               #jump to next map square, OR in x-direction, OR in y-direction
               if sidedistx < sidedisty:
                  sidedistx += deltadistx
                  mapx += stepx
                  side = 0
               else:
                  sidedisty += deltadisty
                  mapy += stepy
                  side = 1
               #Check if ray has hit a wall
               if side == 0:
                   mapval = self.mazemap.getWall(mapx, mapy, mxd)
                   if mapval != None: hit = 1
               else:
                   mapval =  self.mazemap.getWall(mapx, mapy, myd)
                   if mapval != None: hit = 1
            
            #Calculate distance projected on camera direction (oblique distance will give fisheye effect!)
            if side == 0:
                perpwalldist = abs((mapx - rayposx + (1 - stepx) / 2) / raydirx)
            else:
                perpwalldist = abs((mapy - rayposy + (1 - stepy) / 2) / raydiry)
             
            #sort by D^2
            #(rayposx, rayposy) vs (self.position[0], self.position[1])
               
            #Calculate height of line to draw on screen
            if perpwalldist == 0: lineheight = None; drawstart = None; drawend = None
            else:
                lineheight = abs(int(self.screensize[1] / perpwalldist))
                #calculate lowest and highest pixel to fill in current stripe
                drawstart = int(-lineheight / 2 + self.screensize[1] / 2)
                #if drawstart < 0: drawstart = 0
                drawend = int(lineheight / 2 + self.screensize[1] / 2)
            #calculate value of wallX
            wallx = 0 #where exactly the wall was hit
            if side == 1:
               wallx = rayposx + ((mapy - rayposy + (1 - stepy) / 2) / raydiry) * raydirx
            else:
               wallx = rayposy + ((mapx - rayposx + (1 - stepx) / 2) / raydirx) * raydiry
            wallx -= int((wallx))
            
            mu = wallx
            
            #make ex just equal x to mirror the world
            ex = (self.screensize[0]-1)-x
            op[ex] = (lineheight, (drawstart, drawend), mu, mapval)
            
            #WALL
            #(dist^2, 0, xpos, height, (drawstart, drawend), mu, mapval)
            #SPRITE
            #(dist^2, 1, xcenter, height, (drawstart, drawend), scale, mapval)
        return op
            
