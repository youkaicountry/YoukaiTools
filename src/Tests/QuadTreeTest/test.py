from YoukaiTools import QuadTree
from YoukaiTools import Tester
import random

#split and manually verify the first children's regions
#then split one of those and manually test those regions
def testBasicSplit():
   q = QuadTree.QuadTree( (0.0, 0.0, 1.0, 1.0) )
   q.splitNode(0)
   children = q.getNodeChildren(0)
   
   if q.getNodeRegion(children[0]) != (.5, 0.0, 1.0, .5)   : return Tester.Result(False, "Failed On split 1 Q1")
   if q.getNodeRegion(children[1]) != (0.0, 0.0, .5, .5)   : return Tester.Result(False, "Failed On split 1 Q2")
   if q.getNodeRegion(children[2]) != (0.0, 0.5, .5, 1.0)  : return Tester.Result(False, "Failed On split 1 Q3")
   if q.getNodeRegion(children[3]) != (0.5, 0.5, 1.0, 1.0) : return Tester.Result(False, "Failed On split 1 Q4")
   
   children = q.splitNode(children[2]) #split the Q3 node
   
   if q.getNodeRegion(children[0]) != (.25, .5, .5, .75)     : return Tester.Result(False, "Failed On split 2 Q1")
   if q.getNodeRegion(children[1]) != (0.0, .5, .25, .75)    : return Tester.Result(False, "Failed On split 2 Q2")
   if q.getNodeRegion(children[2]) != (0.0, 0.75, .25, 1.0)  : return Tester.Result(False, "Failed On split 2 Q3")
   if q.getNodeRegion(children[3]) != (0.25, 0.75, 0.5, 1.0) : return Tester.Result(False, "Failed On split 2 Q4")
   
   return Tester.Result(True, "Basic Split Passed.")

#test num nodes
#test node removal
   
def testLeaf():
   #have removal in here?
   #verify they all have no children
   #verify that all other nodes DO have children
   #number of leaves should equal 1 + 4*splits - splits = 1 + 3*splits
   q = None
   rleaves = []
   r = random.Random(12345)
   for x in range(100):
      iterations = r.randint(10, 100)
      rleaves = [0]
      q = QuadTree.QuadTree((0.0, 0.0, 1.0, 1.0))
      for x in range(iterations):
         r.shuffle(rleaves)
         nid = rleaves.pop()
         #print(nid)
         rleaves += q.splitNode(nid)
      hypleaves = 1 + (3*iterations)
      testleaves = len(rleaves)
      ql = q.getLeafNodes()
      quadleaves = len(ql)
      if hypleaves != quadleaves : return Tester.Result(False, "Number of leaves in QuadTree (" + str(quadleaves) + ") does not match theoretical (" + str(hypleaves) + ").")
   
      for x in rleaves:
         if x not in ql: return Tester.Result(False, "Node ID (" + str(x) + ") in theoretical leaf list not present in QuadTree's leaf list.")
   
   return Tester.Result(True, "Leaf Test Passed.")
   
   
   
   
t = Tester.Tester()
t.addTest("Basic Split", "Tests node splitting.", testBasicSplit)
t.addTest("Leaves", "Tests that leaf reporting is correct.", testLeaf)
t.doAllTests()

r = t.getAllTests()
for x in r:
   print(str(x))
   print("")
   
q = QuadTree.QuadTree((0.0, 0.0, 1.0, 1.0))
q.splitNode(0)
q.splitNode(2)
print(q.getNodeDepth(6))
print(q.getNodeDepth(3))
print(q.getNodeDepth(0))

