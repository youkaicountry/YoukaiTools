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
from YoukaiTools import ImageTools
from YoukaiTools.ImageTools.FileHandlers import BMP
from YoukaiTools.ImageTools.FileHandlers import PNG

p = ImageTools.LineFont.makeDefaultPathFont()
rp = ImageTools.LineFont.renderPathFontToRasterFont(p, 25)
#ImageTools.FileHandlers.BMP.saveFile("./font.bmp", rp[0]["2"])
ImageTools.FileHandlers.PNG.saveFile("./font.png", rp[0]["2"])

im = ImageTools.Create.newImage(200, 200)
ImageTools.LineFont.writeRasterFontOnImage(im, (5, 5), rp, "AB012101")
#ImageTools.FileHandlers.BMP.saveFile("./text.bmp", im)
ImageTools.FileHandlers.PNG.saveFile("./text.png", im)
