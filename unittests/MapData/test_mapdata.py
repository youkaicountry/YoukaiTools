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

import unittest

from YoukaiTools import MapData

class TestBlockDataTypes(unittest.TestCase):
    def test_blockmappathing(self):
        bmp = MapData.datatypes.BlockMapPathing(8, 8, initval=False)
        self.assertEqual(bmp.getSize(), (8, 8))
        bmp.setSpace(4, 5, True)
        bmp.setSpace(5, 5, True)
        self.assertFalse(bmp.getSpace(1, 4))
        self.assertTrue(bmp.getSpace(4, 5))
        self.assertTrue(bmp.getSpace(5, 5))
        self.assertFalse(bmp.graph.containsVertex((4, 5)))
        self.assertTrue(bmp.graph.containsVertex((1, 4)))
        return

if __name__ == '__main__':
    unittest.main()
    