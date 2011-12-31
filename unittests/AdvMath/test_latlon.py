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

#KIAH to RJTT: 6670 miles

import YoukaiTools.AdvMath
from YoukaiTools.AdvMath import LatLong as LatLong
import unittest

class TestLatLon(unittest.TestCase):
    def test_dist(self):
        #George Bush International in Houston (ICAO: KIAH) to JFK International in New York City (ICAO: KJFK) is
        #around 1418 miles.
        #KIAH is at 29°59′04″N 095°20′29″W
        #KJFK is at 40°38′23″N 073°46′44″W
        kiah = ((29, 59, 4), (95, 20, 29))
        kjfk = ((40, 38, 23), (73, 46, 44))
        self.assertAlmostEquals(LatLong.dist(kiah, kjfk, 3963.14), 1418.0, delta=5.0)
        return
        
if __name__ == '__main__':
    unittest.main()
    