import time
import random

from YoukaiTools import ImageTools

images = [(x+10)*10 for x in range(10)]

r = random.Random("test_seed")

t0 = time.clock()
for ysize in images:
    for xsize in images:
        bgcolor = (r.random(), r.random(), r.random())
        im = ImageTools.Create.newImage(xsize, ysize, bgcolor)
        icolor = ImageTools.ColorModels.invertColor(bgcolor)
        for x in xrange(10000):
            xsm1 = xsize-1
            ysm1 = ysize-1
            #print(x)
            ImageTools.Modify.pset(im, int(r.random()*xsm1), int(r.random()*ysm1), icolor)
            ImageTools.Modify.drawLine(im, int(r.random()*xsm1), int(r.random()*ysm1), int(r.random()*xsm1), int(r.random()*ysm1), icolor)

print("Time Taken: " + str(time.clock()-t0))
