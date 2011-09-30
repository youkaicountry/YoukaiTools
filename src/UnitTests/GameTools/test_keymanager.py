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
    