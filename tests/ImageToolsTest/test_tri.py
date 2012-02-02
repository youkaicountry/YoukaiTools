from YoukaiTools import ImageTools
from YoukaiTools.ImageTools.FileHandlers import PNG
from YoukaiTools.ImageTools import CombineFunctions

im = ImageTools.Create.newImage(256, 256, [0.0, 0.0, 0.0])

ImageTools.Modify.drawFilledTriangle(im, 247, 113, 233, 2, 180, 149, [1.0, 0.0, 0.0])
ImageTools.Modify.drawFilledTriangle(im, 100, 100, 250, 90, 100, 200, [0.0, 1.0, 0.0], CombineFunctions.add)

PNG.saveFile("./tri.png", im)

