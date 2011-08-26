from .. import Create
from .. import SubImage
from .. import Metric
from .. import Comparison
from .. import settings
import AdvFunctions

#returns list of tiles that make up a mosaic, and a list of average colors if requested
#image size should be a multiple of the tile size
def makeMosaic(image, imagepool, usecolor=True, manhattan=1.0, average_col=.25, average_val=.25, manhattanaverage=True):
    settings.vmessage("Mosaic Started.", 0)
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
            index = AdvFunctions.spatial.arrayIndex2To1(x, y, tilesx, 3)
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
