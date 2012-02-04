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

import math

class TileManager:
    def __init__(self, camera2d, width, height, tilemap=None):
        self.camera2d = camera2d
        self.width = width
        self.height = height
        self.tilemap = tilemap
        return
    
    def getShownTiles(self):
        first_x_tile = int(self.camera2d.cameraxmin)
        if first_x_tile < 0: first_x_tile = 0
        first_x_tile_screenloc = self.camera2d.getScreenX(float(first_x_tile))
        tile_dx = self.camera2d.getScreenXDistance(1.0)
        last_x_tile = int(math.ceil(self.camera2d.cameraxmax))+1
        if last_x_tile >= self.width: last_x_tile = self.width-1
        num_x_tiles = last_x_tile - first_x_tile
        
        first_y_tile = int(self.camera2d.cameraymin)
        if first_y_tile < 0: first_y_tile = 0
        first_y_tile_screenloc = self.camera2d.getScreenY(float(first_y_tile))
        tile_dy = self.camera2d.getScreenYDistance(1.0)
        last_y_tile = math.ceil(self.camera2d.cameraymax)
        if last_y_tile > self.height: last_y_tile = self.height
        num_y_tiles = last_y_tile - first_y_tile
        
        return ((first_x_tile, first_x_tile_screenloc, num_x_tiles, tile_dx), (first_y_tile, first_y_tile_screenloc, num_y_tiles, tile_dy))

#tilexparams = (tilewidth, tilewidthborder, tilewidthgrid, tilesacross)
#tileyparams = (tileheight, tileheightborder, tileheightgrid, tilesdown)
class SpriteSheet:
    def __init__(self, tilexparams, tileyparams, cache = False, sheet=None):
        self.tilewidth, self.tilewidthborder, self.tilewidthgrid, self.tilesacross = tilexparams
        self.tileheight, self.tileheightborder, self.tileheightgrid, self.tilesdown = tileyparams
        self.sheet = sheet
        if cache: self.generateCache(tilexparams[3]*tileyparams[3])
        return
    
    def getSprite(self, index):
        x = index%self.tilesacross
        y = index//self.tilesacross
        return (self.tilewidthborder+(self.tilewidth+self.tilewidthgrid)*x, self.tileheightborder+(self.tileheight+self.tileheightgrid)*y)
    
    def getSpriteFromCache(self, index):
        return self.cache[index]
    
    def generateCache(self, sprites):
        self.cache = []
        for i in xrange(sprites):
            self.cache.append(self.getSprite(i))
        return
