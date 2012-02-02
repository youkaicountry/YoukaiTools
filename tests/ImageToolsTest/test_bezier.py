from YoukaiTools import ImageTools
from YoukaiTools.ImageTools.FileHandlers import PNG
from YoukaiTools.ImageTools import CombineFunctions

im = ImageTools.Create.newImage(256, 256, [0.0, 0.0, 0.0])

ImageTools.Modify.drawQuadraticBezier(im, (20, 20), (30, 50), (45, 22), [1.0, 0.0, 0.0])

PNG.saveFile("./bezier.png", im)
