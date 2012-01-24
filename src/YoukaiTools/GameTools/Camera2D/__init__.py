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

from collections import deque

class Camera2D:
    def __init__(self, camerabounds=(0, 0, 10, 10), screensize=(320, 280)):
        self.setCameraBounds(*camerabounds)
        self.setScreenSize(*screensize)
        return
        
    def setScreenSize(self, width, height):
        self.screenwidth = width
        self.screenheight = height
        return
        
    def setCameraBounds(self, xmin, ymin, xmax, ymax):
        self.cameraxmin = xmin
        self.cameraymin = ymin
        self.cameraxmax = xmax
        self.cameraymax = ymax
        return
    
    def getScreenX(self, worldx):
        return ((worldx-self.cameraxmin)/(self.cameraxmax-self.cameraxmin))*self.screenwidth
    
    def getScreenY(self, worldy):
        return ((worldy-self.cameraymin)/(self.cameraymax-self.cameraymin))*self.screenheight
    
    def getScreenLocation(self, worldloc):
        return (self.getScreenX(worldloc[0]), self.getScreenY(worldloc[1]))
    
    def getWorldX(self, screenx):
        return ((screenx/self.screenwidth)*(self.cameraxmax-self.cameraxmin))*self.cameraxmin
    
    def getWorldY(self, screeny):
        return ((screeny/self.screenheight)*(self.cameraymax-self.cameraymin))*self.cameraymin
    
    def getWorldLocation(self, screenloc):
        return (self.getWorldX(screenloc[0]), self.getWorldY(screenloc[1]))
    
    def getScreenXDistance(self, worldxdist):
        return abs(self.getScreenX(0) - self.getScreenX(worldxdist))
    
    def getScreenYDistance(self, worldydist):
        return abs(self.getScreenY(0) - self.getScreenY(worldydist))
    
    def getWorldXDistance(self, screenxdist):
        return abs(self.getWorldX(0) - self.getWorldX(screenxdist))
        
    def getWorldYDistance(self, screenydist):
        return abs(self.getWorldY(0) - self.getWorldY(screenydist))
    
    def moveCamera(self, deltax, deltay):
        self.cameraxmin += deltax
        self.cameraxmax += deltax
        self.cameraymin += deltay
        self.cameraymax += deltay
        return
    
    def scroll(self, dx, dy):
        wdx = (self.cameraxmax - self.cameraxmin) * dx
        hdy = (self.cameraymax - self.cameraymin) * dy
        self.moveCamera(wdx, hdy)
        return
    
    def centerOn(self, x, y):
        cx = .5 * (self.cameraxmin + self.cameraxmax)
        cy = .5 * (self.cameraymin + self.cameraymax)
        dx = x - cx
        dy = y - cy
        self.moveCamera(dx, dy)
        return
    
    #factor > 1.0 zooms in
    #factor < 1.0 zooms out
    def zoom(self, factor):
        oldxl = (self.cameraxmax - self.cameraxmin)
        oldyl = (self.cameraymax - self.cameraymin)
        newxl = oldxl/factor
        newyl = oldyl/factor
        dx = (oldxl-newxl)*.5
        dy = (oldyl-newyl)*.5
        self.setCameraBounds(self.cameraxmin+dx, self.cameraymin+dy, self.cameraxmax-dx, self.cameraymax-dy)
        return

class Camera2DController:
    def __init__(self, camera2d=None):
        
        return
    