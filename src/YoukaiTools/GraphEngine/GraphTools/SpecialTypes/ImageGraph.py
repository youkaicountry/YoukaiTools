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

def buildImageGraph(g, width, height, xwrap, ywrap, channels):
   g.clearGraph()
   g.setEdgeDataSize(0)
   g.setVertexDataSize(channels)
   #add the vertices
   for i in range(width*height):
      g.addVertex()
   #add edges
   for y in range(height):
      for x in range(width):
         v = __getImageIndex(x, y, width)
         connectionlist = [True, True, True, True] #Up, Down, Left, Right
         #construct the connection list and handle wrapping
         if x == 0:
            connectionlist[2] = False
            if xwrap:
               g.addEdge(v, __getImageIndex(width-1, y, width))
         if y == 0:
            connectionlist[0] = False
            if ywrap:
               g.addEdge(v, __getImageIndex(x, height-1, width))

         if x == width-1:
            connectionlist[3] = False
         if y == height-1:
            connectionlist[1] = False
         #Now make the connections

         if connectionlist[0]:
            g.addEdge(v, __getImageIndex(x, y-1, width))
         if connectionlist[1]:
            g.addEdge(v, __getImageIndex(x, y+1, width))
         if connectionlist[2]:
            g.addEdge(v, __getImageIndex(x-1, y, width))
         if connectionlist[3]:
            g.addEdge(v, __getImageIndex(x+1, y, width))
   return
   
def __getImageIndex(x, y, width):
   return y*width + x
