#Copyright (c) <2011-2012> <Nathaniel Caldwell>

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

from math import ceil

class TileManager:
    """
    Manages a tile based map with a camera, for smooth scrolling and zooming.
    """
    def __init__(self, camera2d, width, height, tilemap=None):
        self.camera2d = camera2d
        self.width = width
        self.height = height
        self.tilemap = tilemap
        return
    
    #TODO: figure out why x and y differ...
    def getShownTiles(self):
        """
        Returns the data needed to draw the tiles visible by the camera.
        It returns a tuple containing 2 more tuples, one for x and one for y.
        Each contains the following:
        first_tile - The first tile coordinate visible on that axis.
        first_tile_screenloc - Where on the screen the first tile begins
        num_tiles - how many tiles across/down should be drawn (counting the first tile)
        tile_delta - how far in screen coordinates each tile should be.
        @return: A tuple of tuples as described above.
        @rtype C{iterable}
        """
        first_x_tile = int(self.camera2d.cameraxmin)
        if first_x_tile < 0: first_x_tile = 0
        first_x_tile_screenloc = self.camera2d.getScreenX(float(first_x_tile))
        tile_dx = self.camera2d.getScreenXDistance(1.0)
        last_x_tile = int(ceil(self.camera2d.cameraxmax))+1
        if last_x_tile >= self.width: last_x_tile = self.width-1
        num_x_tiles = last_x_tile - first_x_tile
        
        first_y_tile = int(self.camera2d.cameraymin)
        if first_y_tile < 0: first_y_tile = 0
        first_y_tile_screenloc = self.camera2d.getScreenY(float(first_y_tile))
        tile_dy = self.camera2d.getScreenYDistance(1.0)
        last_y_tile = ceil(self.camera2d.cameraymax)       #different
        if last_y_tile > self.height: last_y_tile = self.height #different
        num_y_tiles = last_y_tile - first_y_tile
        
        return ((first_x_tile, first_x_tile_screenloc, num_x_tiles, tile_dx), (first_y_tile, first_y_tile_screenloc, num_y_tiles, tile_dy))

#tilexparams = (tilewidth, tilewidthborder, tilewidthgrid, tilesacross)
#tileyparams = (tileheight, tileheightborder, tileheightgrid, tilesdown)
class SpriteSheet:
    """
    Represents an image with sprites arranged in a grid.
    """
    def __init__(self, tilexparams, tileyparams, cache = True, sheet=None):
        """
        Initializes the sprite sheet objects. It takes tilexparams and tileyparams, which specify the layout of the
        sprites in the image. Each one should be a tuple with the following data:
        (tilewidth, widthborder, widthgrid, num)
        tilewidth - how many pixels wide each sprite is
        widthborder - how many pixels wide/tall the border is (0 if no border)
        widthgrid - how many pixels wide/tall the grid between sprites is (0 if no grid)
        num - how many sprites across/down the image contains
        @param tilexparams: A tuple as described above, specifying the x axis
        @param tileyparams: A tuple as described above, specifying the y axis
        @param cache: Whether to cache the tiles lookup, which gives a small speed gain
        @type cache: C{bool}
        @param sheet: Arbitrary data (such as the image object) can be attached here.
        """
        self.tilewidth, self.tilewidthborder, self.tilewidthgrid, self.tilesacross = tilexparams
        self.tileheight, self.tileheightborder, self.tileheightgrid, self.tilesdown = tileyparams
        self.sheet = sheet
        if cache: 
            self.__generateCache(tilexparams[3]*tileyparams[3])
            self.getSprite = self.__getSpriteFromCache
        return
    
    def getSprite(self, index):
        """
        Given the index of a sprite, returns the x and y location of the upper left on the sprite sheet
        @param index: The index of sprite for which to retrieve coordinates.
        @return: The location of the upper-left of the requested tile.
        @rtype: C{iterable}
        """
        x = index%self.tilesacross
        y = index//self.tilesacross
        return (self.tilewidthborder+(self.tilewidth+self.tilewidthgrid)*x, self.tileheightborder+(self.tileheight+self.tileheightgrid)*y)
    
    def __getSpriteFromCache(self, index):
        return self.cache[index]
    
    def __generateCache(self, sprites):
        self.cache = []
        for i in xrange(sprites):
            self.cache.append(self.getSprite(i))
        return
