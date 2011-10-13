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
from YoukaiTools.Raycast import PyGameOutput
from YoukaiTools import MazeGen
from YoukaiTools.MazeGen.generators import maze as maze
import sys

pygame.init()
size = width, height = 640, 480
speed = [2, 2]
bg = 0, 0, 0
screen = pygame.display.set_mode(size)
pygame.time.set_timer(pygame.USEREVENT, 40)

#make the maze
mg = maze.recursiveBacktrackMaze()
mg.make(100, 100, 0, 0, 0, None)
bm = mg.get("blockmap")
m = MazeGen.convert.blockMap2MazeMap(bm)



R = Raycast.RaycastMaze(m, size)

R.setPosition((1.5, 1.5))
R.turn(.8)

R.setCollision(0, True)

PG = PyGameOutput.PyGameOutput(size)
PG.addTile("./wall1.jpg", 0)
PG.addTile("./wall2.jpg", 1)

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
           R.turn(.1)
        if keys[pygame.K_LEFT] == True:
           R.turn(-.1)
        if keys[pygame.K_UP] == True:
           R.move(.1)
        if keys[pygame.K_DOWN] == True:
           R.move(-.1)
        
        screen.fill(bg)
        rr = R.raycast()
        PG.drawScreen(screen, rr)
        
        #screen.fill(bg)
        
        pygame.display.flip()
