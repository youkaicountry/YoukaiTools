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

from .. import SubImage
import YoukaiTools.AdvMath
import YoukaiTools.PyRange

#the incoming image should be cleaned up and rotated already at this point,
#may fix that later
#barcode is read from the center
#returns an array of 0's (narrow) and 1's (wide)
#image - the image file, already cleaned
#reach - average weight average above and below each space
def read1DBarcode(image, weights=[1.0, 1.0, 1.0, .9, .9, .8, .8]):
    #CLEAN UP WOULD BE HERE
    
    vimage = SubImage.averageChannels(image)
    #reach_sum = sum(reach) #the sum of the weights
    
    #PICK LINES WOULD BE HERE
    linesy = [int(image[1]/2)]
    m = -1
    ind = 0
    for i in range(len(weights)-1):
        linesy.append(linesy[0] + (m*(ind+1)))
        if m == 1: ind += 1
        m *= -1
    #print(linesy)
    
    __scanLines(vimage, linesy, weights)
    return

#takes a grayscale image
def __scanLines(image, lines, weights):
    points = []
    div = sum(weights)
    for x in range(image[0]):
        adder = 0.0
        for i, y in enumerate(lines):
            ind = YoukaiTools.AdvMath.Indices.arrayIndex2To1(x, y, image[0], 3)
            adder += image[ind][0]*weights[i]
        adder /= div
        points.append([x, adder])
    dg = YoukaiTools.PyRange.DataGraph.DataGraph1D()
    dg.setFromPoints(points)
    return
