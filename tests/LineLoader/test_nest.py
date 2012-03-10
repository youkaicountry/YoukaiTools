from YoukaiTools import LineLoader

f=open("./nested.txt", "r")
l = LineLoader.loadNestedConfig(f)
print(l)
