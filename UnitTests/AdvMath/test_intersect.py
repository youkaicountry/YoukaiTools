import YoukaiTools.AdvMath
from YoukaiTools.AdvMath import Intersect as Intersect
import unittest

class TestRect(unittest.TestCase):
    def test_rectXRect(self):
        testc = ( (([10, 10, 20, 20], [15, 12, 22, 24], False),True), (([8, 14, 3, 7], [16, 18, 5, 10], False),False), (([0, 2, 0, 2], [2, 4, 0, 2], False),False), (([1, 2, 3, 4], [2, 3, 5, 6], True),(True,(2,3,3,4))) )
        for c in testc:
            self.assertEquals(Intersect.rectxRect(*c[0]), c[1])
        return
        
if __name__ == '__main__':
    unittest.main()
    
