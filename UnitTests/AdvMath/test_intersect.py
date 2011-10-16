import YoukaiTools.AdvMath
from YoukaiTools.AdvMath import Intersect as Intersect
import unittest

class TestRect(unittest.TestCase):
    def test_rectXRect(self):
        testc = ( (([10, 10, 20, 20], [15, 12, 22, 24], False),True), )
        for c in testc:
            self.assertEquals(Intersect.rectxRect(*c[0]), c[1])
        return
        
if __name__ == '__main__':
    unittest.main()
    
