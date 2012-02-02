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

from YoukaiTools.AdvMath.Indices import arrayIndex2To1

from . import Create
from . import Modify
from . import CombineFunctions

#return a new image with combined the channels
#can be used to create an image from a single channel, or to
#average the values of certain channels together
#if channels == None, then it is the straight average value
def averageChannels(image, channels=None):
    if channels is None:
        use_channels = [i for i in range(image[2])]
    else:
        use_channels = channels
    div = len(use_channels)
    outimage = Create.newImage(image[0], image[1], [0])
    for i in xrange(image[0]*image[1]):
        j = i+3
        adder = 0.0
        for c in use_channels:
            adder += image[j][c]
        outimage[j][0] = adder / div
    return outimage

#return a new image that is a subset of the given image
def getSubImage(image, x, y, width, height):
    outimage = Create.newImage(width, height, 0, image[2])
    oi = 3
    for ty in xrange(height):
        for tx in xrange(width):
            i = arrayIndex2To1(tx+x, ty+y, image[0], 3)
            outimage[oi] = image[i][:]
            oi += 1
    return outimage

#returns a new image that is a clone of the given
def clone(image):
    outimage = Create.newImage(image[0], image[1], 0, image[2])
    for i, x in enumerate(image[3:]):
        j = i+3
        outimage[j] = image[j][:]
    return outimage

#breaks an image into tiles and returns an imagepool of them
#TODO: Have tilesx and tilesy = None revert to the maximum allowed
def getTiles(image, tilexsize, tileysize, tilesx, tilesy, xbordersize=0, ybordersize=0, xboundarysize=0, yboundarysize=0):
    imagepool = []
    for ytile in xrange(tilesy):
        for xtile in xrange(tilesx):
            x = xbordersize + (xtile*tilexsize) + (xtile*xboundarysize)
            y = ybordersize + (ytile*tileysize) + (ytile*yboundarysize)
            print(x, y)
            imagepool.append(getSubImage(image, x, y, tilexsize, tileysize))
    return imagepool

#constructs an image of tiles
#time_map is an image with 1 channel of integers representing indices
#of images in the imagepool
def tileImage(imagepool, tile_map, colormap=None, tintcombine=CombineFunctions.multiply, tintcparams=[]):
    outimage = Create.newImage(tile_map[0]*imagepool[0][0], tile_map[1]*imagepool[0][1], initialcolor=0, channels=imagepool[0][2])
    for tmy in xrange(tile_map[1]):
        for tmx in xrange(tile_map[0]):
            i = arrayIndex2To1(tmx, tmy, tile_map[0], 3)
            if colormap != None:
                tile = clone(imagepool[tile_map[i][0]])
                Modify.applyColor(tile, colormap[i], tintcombine, tintcparams)
                Modify.overlay(outimage, tile,  tmx*imagepool[0][0], tmy*imagepool[0][1])
            else:
                Modify.overlay(outimage, imagepool[tile_map[i][0]], tmx*imagepool[0][0], tmy*imagepool[0][1])
    return outimage

def verticalFlip(image):
    outimage = Create.newImage(image[0], image[1], 0, image[2])
    for y in xrange(image[1]):
        ny = (image[1]-1) - y
        for x in xrange(image[0]):
            inew = arrayIndex2To1(x, ny, image[0], 3)
            iold = arrayIndex2To1(x, y, image[0], 3)
            outimage[iold] = image[inew][:]
    return outimage

#splits the given image into new images by channel:
#for example, splitparams=([0,2], [1], [1,2]) would make 3 images
def splitChannels(image, splitparams):
    outpool = []
    for i in xrange(len(splitparams)):
        outpool.append(Create.newImage(image[0], image[1], 0, len(splitparams[i])))
    for i, x in enumerate(image[3:]):
        for j, sp in enumerate(splitparams):
            for k, c in enumerate(sp):
                outpool[j][i+3][k] = x[c]
    return outpool

#combineparams should be ([im#, channel], [...], ...)
def combineChannels(images, combineparams):
    out = Create.newImage(images[0][0], images[0][1], 0, len(combineparams))
    for i, x in enumerate(out[3:]):
        k = i+3
        for j, c in enumerate(combineparams):
            out[k][j] = images[c[0]][k][c[1]]
    return out

def shrinkImage(image, newwidth, newheight):
    xgridsize = int(image[0] / newwidth)
    ygridsize = int(image[1] / newheight)
    outimage = Create.newImage(newwidth, newheight, 0, image[2])
    t = []
    div = xgridsize*ygridsize
    for gy in xrange(newheight):
        for gx in xrange(newwidth):
            xstart = gx * xgridsize
            xend = xstart + xgridsize
            ystart = gy * ygridsize
            yend = ystart + ygridsize
            t = [0 for x in range(image[2])]
            for py in xrange(ystart, yend):
                for px in xrange(xstart, xend):
                    index = arrayIndex2To1(px, py, image[0], 3)
                    for i, c in enumerate(image[index]):
                        t[i] += c
            for i in range(len(t)):
                t[i] /= div
            nindex = arrayIndex2To1(gx, gy, newwidth, 3)
            outimage[nindex] = t[:]
    return outimage
