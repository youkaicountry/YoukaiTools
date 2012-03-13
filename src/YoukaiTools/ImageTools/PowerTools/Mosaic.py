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

from .. import Create
from .. import SubImage
from .. import Metric
from .. import Comparison
from .. import settings
import YoukaiTools.AdvMath

#returns list of tiles that make up a mosaic, and a list of average colors if requested
#image size should be a multiple of the tile size
def makeMosaic(image, imagepool, usecolor=True, manhattan=1.0, average_col=.25, average_val=.25, manhattanaverage=True):
    settings.vmessage("Mosaic Started.", 0)
    #clip the image if needed
    cwidth = int(image[0] / imagepool[0][0])
    cheight = int(image[1] / imagepool[0][1])
    if (cwidth != image[0]) or (cheight != image[1]):
        image = SubImage.getSubImage(image, 0, 0, cwidth, cheight)
    tilesx = int(image[0] / imagepool[0][0]) #get the number of tiles wide
    tilesy = int(image[1] / imagepool[0][1]) #get the number of tiles high
    tilewidth = imagepool[0][0]
    tileheight = imagepool[0][1]
    average_color = Create.newImage(tilesx, tilesy, 0, image[2])
    tile_map = Create.newImage(tilesx, tilesy, [0])
    use_imagepool = imagepool
    poolaveragecolor = []
    bw_imagepool = []
    bw_avg = None
    if average_val > 0 or usecolor == False:
        for im in imagepool:
            bw_imagepool.append(SubImage.averageChannels(im))
        if average_val > 0:
            bw_avg = []
            for im in bw_imagepool:
                bw_avg.append(Metric.calculateAverageColor(im))
    else:
        bw_imagepool = None
    for pim in imagepool:
        poolaveragecolor.append(Metric.calculateAverageColor(pim))
    if usecolor == False:
        bw_tile_map = Create.newImage(tilesx, tilesy, [0])
        use_imagepool = bw_imagepool
    for y in range(tilesy):
        for x in range(tilesx):
            nx = tilewidth*x
            ny = tileheight*y
            #get the sub image
            si = SubImage.getSubImage(image, nx, ny, tilewidth, tileheight)
            ac = Metric.calculateAverageColor(si)
            index = YoukaiTools.AdvMath.Indices.arrayIndex2To1(x, y, tilesx, 3)
            #print(index)
            average_color[index] = ac[:]
            if usecolor == False:
                #get the value image of the subimage
                si = SubImage.averageChannels(si)
                ac = Metric.calculateAverageColor(si)
                vi = si
                iavc = ac
            else:
                if average_val > 0:
                    vi = SubImage.averageChannels(si)
                    iavc = Metric.calculateAverageColor(vi)
                else:
                    vi = None
                    iavc = None
            tile_map[index][0] = Comparison.matchImages(si, use_imagepool, manhattan, average_col, average_val, ac, poolaveragecolor, vi, iavc, bw_imagepool, bw_avg, manhattanaverage)[0]
    return (tile_map, average_color)
