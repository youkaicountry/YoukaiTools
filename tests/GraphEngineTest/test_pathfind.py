import YoukaiTools.GraphEngine as GraphEngine
import YoukaiTools.GraphEngine.GraphTools.Paths as Paths
import YoukaiTools.MazeGen.datatypes
import YoukaiTools.GraphEngine.GraphTools.SpecialTypes.GridGraph as GridGraph

graph = GraphEngine.BasicGraph()
bmap = YoukaiTools.MazeGen.datatypes.BlockMap(5, 5)
bmap.setSpaces([(2, 0), (2, 1), (2, 2), (2, 4)], True)
GridGraph.buildGridGraphFromBlockMap(graph, bmap)
path = Paths.AStarPath(graph, (0, 0), (4, 0))

sp = Paths.makeSpatialPath2D(graph, path)

for i in range(101):
    ii = float(i)/100.0
    print(sp.getIValue(ii))
    