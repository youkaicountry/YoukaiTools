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
