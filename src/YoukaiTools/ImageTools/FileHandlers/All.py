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

from . import PNG
from . import BMP

iformat = {}
iformat["png"] = PNG
iformat["bmp"] = BMP

def getFormatName(filename):
    return filename.split(".")[-1].lower()

def getFormat(filename):
    return iformat[filename.split(".")[-1].lower()]

def loadFile(filename, uh=None):
    f = open(filename, "rb")
    uformat = getFormat(filename)
    o = uformat.load(f)
    f.close()
    return o

def saveFile(filename, image, uh=None):
    f = open(filename, "wb")
    uformat = getFormat(filename)
    uformat.save(f, image, uh)
    f.close()
    return

def save(f, image, format="png", uh=None):
    iformat[format].save(f, image, uh)
    return

def load(f, image, format="png", uh=None):
    iformat[format].load(f, image, uh)
    return
