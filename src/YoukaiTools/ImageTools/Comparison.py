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

from . import Metric
from . import SubImage

#OPTIMIZE: HAVE PRECOMPUTED VALUES ABLE TO BE FED IN TO THESE FUNCTIONS

#returns the manhattan distance between the two images of the same width and height
#and number of channels
def manhattanDistance(image1, image2):
    adder = 0
    for i in xrange(3, len(image1)):
        for j in xrange(image1[2]):
            adder += abs(image1[i][j] - image2[i][j])
    return adder
    
def manhattanAverageDistance(image1, image2, div=None):
    adder = 0
    if div==None:
        div = image1[0]*image1[1]
    for i in range(3, len(image1)):
        for j in xrange(image1[2]):
            adder += abs(image1[i][j] - image2[i][j])
    return adder/div

#must have same number of channels
def averageColorDist(image1, image2, averagecolor1=None, averagecolor2=None):
    a1 = Metric.calculateAverageColor(image1) if averagecolor1 is None else averagecolor1
    a2 = Metric.calculateAverageColor(image2) if averagecolor2 is None else averagecolor2
    adder = 0
    for i in xrange(len(a1)):
        adder += abs(a1[i] - a2[i])
    return adder

def averageValueDist(image1, image2, valueimage1=None, valueimage2=None, averagevcolor1=None, averagevcolor2=None):
    ni1 = SubImage.averageChannels(image1) if valueimage1 is None else valueimage1
    ni2 = SubImage.averageChannels(image2) if valueimage2 is None else valueimage2
    a1 = Metric.calculateAverageColor(ni1) if averagevcolor1 is None else averagevcolor1
    a2 = Metric.calculateAverageColor(ni2) if averagevcolor2 is None else averagevcolor2
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
    for i in xrange(len(imagepool)):
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
