#interface:
#getNodeByLocation(x, y) - returns nodeID
#splitNode(id)
#getNodeRegion(id)
#getNumNodes
#getWorldRegion - simply returns node 0 region
#getHierarchy - returns list of all nodes in hierarchy
#joinNodes(id) - joins nodes and all of their siblings. Collapses everything under.
#getChildren(id)
#getParent(id)
#getAllLeafNodes()

#add data like in the GraphEngine


#for each node, save region, parent, children

#quadrant lookup
#quadlook[leftofhalfx?, abovehalfy?]

#have max depth, and also max hits contained in a leaf before it splits itself
quadlook = []
quadlook.append([4, 1])
quadlook.append([3, 2])

class QuadTree:
   #region = (x1, y1, x2, y2) in float
   def __init__(self, region):
      self.x1, self.y1, self.x2, self.y2 = self.region = region
      self.nodes = {}
      self.top = 0
      self.__makeNode(None, region)
      self.leafnodes = set() #points to all of the lead nodes
      self.leafnodes.add(0)
      return
   
   #You can only split a leaf node. (That node has no children/is pointed to by leafnodes)   
   def splitNode(self, nid):
      if nid not in self.leafnodes: return #was not a leaf node
      #get the node info
      node = self.nodes[nid]      #the node
      noder = node.getRegion()    #the node's region
      nx1, ny1, nx2, ny2 = noder  #the individual elements
      #calculate the halfway points
      hx = ((nx2 - nx1) / 2.0) + nx1 #X halfway mark
      hy = ((ny2 - ny1) / 2.0) + ny1 #Y halfway mark
      #make the nodes
      q1 = self.__makeNode(nid, (hx, ny1, nx2, hy)) #upper right (Quadrant 1)
      q2 = self.__makeNode(nid, (nx1, ny1, hx, hy)) #upper left  (Quadrant 2)
      q3 = self.__makeNode(nid, (nx1, hy, hx, ny2)) #lower left  (Quadrant 3)
      q4 = self.__makeNode(nid, (hx, hy, nx2, ny2)) #lower right (Quadrant 4)
      #set them as the children of the split node
      node.setChildren( (q1, q2, q3, q4) )
      #change leafnode info
      self.leafnodes.remove(nid) #remove old
      self.leafnodes.add(q1)
      self.leafnodes.add(q2)
      self.leafnodes.add(q3)
      self.leafnodes.add(q4)
      return (q1, q2, q3, q4)
      
   def getNodeRegion(self, nid):
      return self.nodes[nid].getRegion() 
      
   def getNodeDepth(self, nid):
      pid = self.nodes[nid].getParent()
      depth = 0
      while pid != None:
         pid = self.nodes[pid].getParent()
         depth += 1
      return depth 
   
   def getNodeByLocation(self, location):
      #test if location is out of origin region first...
      
      currentnode = 0
      while currentnode not in self.leafnodes:
         q = self.__getQuadrant(location, self.nodes[currentnode].getRegion())
         currentnode = self.getNodeChildren(currentnode)[q-1]
      return currentnode
      
   #returns in form of (q1, q2, q3, q4), or none if a leaf
   def getNodeChildren(self, nid):
      if nid in self.leafnodes : return None
      node = self.nodes[nid]
      return node.getChildren()
      
   def getLeafNodes(self):
      return tuple([x for x in self.leafnodes])
   
   def __getQuadrant(self, location, region):
      hx = ((region[2] - region[0]) / 2.0) + region[0] #X halfway mark
      hy = ((region[3] - region[1]) / 2.0) + region[1] #Y halfway mark
      lx = location[0] < hx
      ay = location[1] < hy
      return quadlook[lx][ay]
      
   def __makeNode(self, parent, region):
      self.nodes[self.top] = Node(parent, region)
      self.nodes[self.top].setChildren
      out = self.top
      self.top += 1
      return out

#region is (x1, y1, x2, y2)      
class Node:
   def __init__(self, parentid, region):
      self.parentid = parentid
      self.region = region
      self.childQ1 = None
      self.childQ2 = None
      self.childQ3 = None
      self.childQ4 = None
      return
   
   def getRegion(self):
      return self.region
   
   def getParent(self):
      return self.parentid
   
   #give as [Q1, Q2, Q3, Q4]
   def setChildren(self, childrenids):
      self.childQ1, self.childQ2, self.childQ3, self.childQ4 = childrenids
      return
      
   def getChildren(self):
      return (self.childQ1, self.childQ2, self.childQ3, self.childQ4)
      
   def setChildQ1(self, q1):
      self.childQ1 = q1
      return
      
   def setChildQ2(self, q2):
      self.childQ2 = q2
      return
      
   def setChildQ3(self, q3):
      self.childQ3 = q3
      return
      
   def setChildQ4(self, q4):
      self.childQ4 = q4
      return
      
   def clearChildren(self):
      self.childQ1 = None
      self.childQ2 = None
      self.childQ3 = None
      self.childQ4 = None
      return
       
