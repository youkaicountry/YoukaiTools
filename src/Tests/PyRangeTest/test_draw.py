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

from YoukaiTools import PyRange
from YoukaiTools.PyRange.Draw import Draw1D
dg = PyRange.DataGraph1D()

#irregular
#dg.setFromPoints([ (0.0, .8), (1.2, .4), (3.0, .3), (5.2, .45), (6.0, .1), (7.22, .5), (7.6, .7), (8.0, .9) ])

#regular
dg.setFromPoints([ (1.0, 3.3), (2.0, 1.2), (3.0, 1.8), (4.0, 1.1), (5.0, 3.6), (6.0, .08), (7.0, 2.3), (8.0, 1.6) ])

s = Draw1D.makeDefaultSettings()
s["interpolation"] = PyRange.Interpolation.hermite
s["tension"] = 0
s["bias"] = 0
s["maxcolor"] = (1.0, 0.0, 0.0)
s["mincolor"] = (1.0, 0.0, 0.0)
s["markpoints"] = True
Draw1D.saveDataGraph1DFile("dg1d.png", dg, settings=s)
