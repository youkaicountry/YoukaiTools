from YoukaiTools import GraphEngine
import random
from YoukaiTools.GraphEngine.GraphTools.SpecialTypes import Hanoi

#make the basic setup
bg = GraphEngine.Graphs.BasicGraph()

Hanoi.makeHanoi(bg, 3)

GraphEngine.Draw.drawSimple(bg, "./output/hanoi.png", smallwidth=512, layers=[("vertex", .007, ("color", (1.0, 0, 0))), ("edge", ("color", (0, 0, 1.0))), ("vname", 10, (4, -15), None, [1, 1, 1] ) ] )
