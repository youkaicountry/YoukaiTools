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

import pygame
from YoukaiTools import Raycast
from YoukaiTools import PyRange
from YoukaiTools.Raycast import PyGameOutput
from YoukaiTools import MazeGen
from YoukaiTools.MazeGen.generators import maze as maze
import sys

pygame.init()
size = width, height = 640, 480
bg = 0, 0, 0
screen = pygame.display.set_mode(size)
pygame.time.set_timer(pygame.USEREVENT, 40)

#make the maze
a = MazeGen.convert.loadArray("testmap.txt")
bm = MazeGen.convert.array2BlockMap(a)
m = MazeGen.convert.blockMap2MazeMap(bm)

#amap = []
#amap.append([0,  0, 0,   2,   0,   0])
#amap.append([0,None,None,None,None,3])
#amap.append([4,None,6,   None,None,3])
#amap.append([4,None,None,None,None,3])
#amap.append([4,4,   7,   5,   1,   3])
#m = MazeGen.convert.array2MazeMap(amap)

#mg = maze.recursiveBacktrackMaze()
#mg.make((100, 100, 0, 0, 0, None))
#bm = mg.get("blockmap")
#m = MazeGen.convert.blockMap2MazeMap(bm)

fx = [0, 1]
fy = [0, 1]
mg = PyRange.DataGraph1D()
mg.setFromXY(fx, fy)
fx2 = [0, .45, .55, 1]
fy2 = [0, .25, .25, 0]
blg = PyRange.DataGraph1D()
blg.setFromXY(fx2, fy2)


R = Raycast.RaycastMaze(m, size)
R.setMovingGraph(mg, interp=PyRange.Interpolation.hermite, tension=.6)
R.setTurningGraph(mg, interp=PyRange.Interpolation.hermite, tension=.6)
R.setBlockedGraph(blg, interp=PyRange.Interpolation.cosine)

R.setPosition((1.5, 1.5))
R.turn(-1.570796)

R.setCollision(0, True)
R.setCollision(1, True)
R.setCollision(2, True)
R.setCollision(3, True)
R.setCollision(4, True)
R.setCollision(5, True)
R.setCollision(6, True)
R.setCollision(7, True)

PG = PyGameOutput.PyGameOutput(size)
PG.addTile("./images/bluestone.png", 0)
PG.addTile("./images/colorstone.png", 1)
PG.addTile("./images/eagle.png", 2)
PG.addTile("./images/greystone.png", 3)
PG.addTile("./images/mossy.png", 4)
PG.addTile("./images/purplestone.png", 5)
PG.addTile("./images/redbrick.png", 6)
PG.addTile("./images/wood.png", 7)

while True:
    go = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.USEREVENT: go = 1

    if go == 1:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] == True:
           pygame.event.post(pygame.event.Event(pygame.QUIT))
        if keys[pygame.K_RIGHT] == True:
           R.startTurn(12, 1)
        if keys[pygame.K_LEFT] == True:
           R.startTurn(12, -1)
        if keys[pygame.K_UP] == True:
           R.startMove(12, 1)
        if keys[pygame.K_DOWN] == True:
           R.startMove(12, -1)
        
        R.updateStep()
        
        screen.fill(bg)
        rr = R.raycast()
        PG.drawScreen(screen, rr)
        
        #screen.fill(bg)
        
        pygame.display.flip()
