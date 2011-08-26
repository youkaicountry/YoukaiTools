from YoukaiTools import PyRange

bc = PyRange.Paths.BezierCurveCubic()
#print(bc.getLength())

cp = PyRange.Paths.ContainerPath()
cp.addPiece(bc, (0, 0))
print(cp.getIValue(.52))

print(PyRange.Ranges.rangeToRange(8.0, 1.0, 10.0, 1.0, 0.0))
