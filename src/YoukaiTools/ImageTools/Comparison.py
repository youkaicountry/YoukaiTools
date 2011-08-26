from . import Metric
from . import SubImage

#OPTIMIZE: HAVE PRECOMPUTED VALUES ABLE TO BE FED IN TO THESE FUNCTIONS

#returns the manhattan distance between the two images of the same width and height
#and number of channels
def manhattanDistance(image1, image2):
    adder = 0
    for i in range(3, len(image1)):
        for j in range(image1[2]):
            adder += abs(image1[i][j] - image2[i][j])
    return adder
    
def manhattanAverageDistance(image1, image2, div=None):
    adder = 0
    if div==None:
        div = image1[0]*image1[1]
    for i in range(3, len(image1)):
        for j in range(image1[2]):
            adder += abs(image1[i][j] - image2[i][j])
    return adder/div

#must have same number of channels
def averageColorDist(image1, image2, averagecolor1=None, averagecolor2=None):
    a1 = Metric.calculateAverageColor(image1) if averagecolor1 == None else averagecolor1
    a2 = Metric.calculateAverageColor(image2) if averagecolor2 == None else averagecolor2
    adder = 0
    for i in range(len(a1)):
        adder += abs(a1[i] - a2[i])
    return adder

def averageValueDist(image1, image2, valueimage1=None, valueimage2=None, averagevcolor1=None, averagevcolor2=None):
    ni1 = SubImage.averageChannels(image1) if valueimage1 == None else valueimage1
    ni2 = SubImage.averageChannels(image2) if valueimage2 == None else valueimage2
    a1 = Metric.calculateAverageColor(ni1) if averagevcolor1 == None else averagevcolor1
    a2 = Metric.calculateAverageColor(ni2) if averagevcolor2 == None else averagevcolor2
    return averageColorDist(ni1, ni2)

#given an image and an image pool, return the (index,fitvalue) of the image that fits best
#they should all be the same size
def matchImages(image, imagepool, manhattan=1.0, average_color=.25, average_value=.25, iaveragecolor=None, poolaveragecolor=None, ivalueimage=None, iaveragevcolor=None, poolvalueimage=None, poolaveragevcolor=None, manhattanaverage=True):
    first = True
    bestfitindex = 0
    bestfitvalue = 0
    if manhattanaverage: div = image[0]*image[1]
    pac=[None]*len(imagepool) if poolaveragecolor==None else poolaveragecolor
    pvi=[None]*len(imagepool) if poolvalueimage==None else poolvalueimage
    pavc=[None]*len(imagepool) if poolaveragevcolor==None else poolaveragevcolor
    for i in range(len(imagepool)):
        v = 0
        if manhattan > 0:
            v += ((manhattanDistance(image, imagepool[i]))) * (1.0/manhattan) if not manhattanaverage else manhattanAverageDistance(image, imagepool[i], div) * (1.0/manhattan)
        if average_color > 0:
            v += ((averageColorDist(image, imagepool[i], iaveragecolor, pac[i]))) * (1.0/average_color)
        if average_value > 0:
            v += ((averageValueDist(image, imagepool[i], ivalueimage, pvi[i], iaveragevcolor, pavc[i]))) * (1.0/average_value)
        if v < bestfitvalue or first == True:
            first = False
            bestfitvalue = v
            bestfitindex = i
    return (bestfitindex, bestfitvalue)
