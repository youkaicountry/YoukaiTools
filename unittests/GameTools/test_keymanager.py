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
import YoukaiTools.GameTools as GameTools

class TestKeyManager(unittest.TestCase):
    def setUp(self):
        self.km = GameTools.KeyManager(["a", "b", "c", "d", "e"])
        return
    
    def tearDown(self):
        return
    
class TestBasicKeystate(TestKeyManager):
    def test_basic_keystate(self):
        v = self.km.update_from_keyset(keyset=set())
        self.assertEqual(len(v), 0)
        self.assertItemsEqual(v, [])
        
        v = self.km.update_from_keyset(keyset=set(["b", "d"])) #b_down, d_down
        self.assertEqual(len(v), 2)
        self.assertItemsEqual(v, ["d_down", "b_down"])
        
        v = self.km.update_from_keyset(keyset=set(["b", "d", "e"])) #e_down
        self.assertEqual(len(v), 1)
        self.assertItemsEqual(v, ["e_down"])
        
        v = self.km.update_from_keyset(keyset=set(["b", "e"])) #d_up
        self.assertEqual(len(v), 1)
        self.assertItemsEqual(v, ["d_up"])
        
        self.km.update_from_keyset(keyset=set(["b"])) #e_up
        self.km.update_from_keyset(keyset=set(["a"])) #a_down, b_up
        self.km.update_from_keyset(keyset=set()) #a_up

if __name__ == '__main__':
    unittest.main()
    